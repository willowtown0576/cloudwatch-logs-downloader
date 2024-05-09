import boto3
import csv
import argparse
from datetime import datetime


def get_logs(log_group_name, start_time, end_time, profile_name, limit):
    """
    指定されたプロファイルとロググループ名でログを取得します。

    Args:
        log_group_name (str): CloudWatchロググループ名。
        start_time (datetime): 取得開始日時。
        end_time (datetime): 取得終了日時。
        profile_name (str): AWSプロファイル名。
        limit (int): 取得するログの最大数。

    Returns:
        list: 取得したログデータのリスト。
    """
    session = boto3.Session(profile_name=profile_name)
    client = session.client('logs')
    start_query_response = client.start_query(
        logGroupName=log_group_name,
        startTime=int(start_time.timestamp()),
        endTime=int(end_time.timestamp()),
        queryString="fields @timestamp, @message | sort @timestamp desc",
        limit=limit
    )
    query_id = start_query_response['queryId']
    response = None

    # クエリの実行が完了するまで待機
    while response is None or response['status'] == 'Running':
        print("Waiting for query to complete...")
        response = client.get_query_results(queryId=query_id)

    return response['results']


def save_to_csv(logs, filename):
    """
    取得したログをCSVファイルに保存します。

    Args:
        logs (list): ログデータのリスト。
        filename (str): 保存するCSVファイルの名前。
    """
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Message'])
        for log in logs:
            timestamp = datetime.fromtimestamp(int(log[0]['value'])/1000).isoformat()
            message = log[1]['value']
            writer.writerow([timestamp, message])


def main():
    """
    メイン関数: 引数を解析し、指定された条件でログを取得してCSVに保存します。
    """
    parser = argparse.ArgumentParser(description="CloudWatchログを取得してCSVに保存します。")
    parser.add_argument("--log-group", required=True, help="CloudWatchロググループ名を指定します。")
    parser.add_argument("--profile", required=True, help="使用するAWSプロファイル名を指定します。")
    parser.add_argument("--start-date", required=True, help="取得開始日時を YYYY-MM-DDTHH:MM:SS 形式で指定します。")
    parser.add_argument("--end-date", required=True, help="取得終了日時を YYYY-MM-DDTHH:MM:SS 形式で指定します。")
    parser.add_argument("--output-file", default="output.csv", help="保存するCSVファイルの名前を指定します。")
    parser.add_argument("--limit", type=int, default=10000, help="取得するログの最大数を指定します。")
    parser.add_argument("--no-limit", action='store_true', help="ログの取得数に上限を設定しない場合に指定します。")
    args = parser.parse_args()

    limit = None if args.no_limit else args.limit
    start_time = datetime.strptime(args.start_date, "%Y-%m-%dT%H:%M:%S")
    end_time = datetime.strptime(args.end_date, "%Y-%m-%dT%H:%M:%S")

    logs = get_logs(args.log_group, start_time, end_time, args.profile, limit)
    save_to_csv(logs, args.output_file)
    print(f"Logs have been saved to {args.output_file}")

if __name__ == '__main__':
    main()
