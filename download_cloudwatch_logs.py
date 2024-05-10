import boto3
import csv
import json
import argparse
from datetime import datetime


def get_events(log_group_name, start_time, end_time, profile_name, verify_ssl):
    """
    指定されたプロファイルとロググループ名でログを取得します。

    Args:
        log_group_name (str): CloudWatchロググループ名。
        start_time (datetime): 取得開始日時。
        end_time (datetime): 取得終了日時。
        profile_name (str): AWSプロファイル名。
        verify_ssl (bool): 

    Yield:
        list: 取得したログデータのリスト。
    """
    session = boto3.Session(profile_name=profile_name)
    client = session.client('logs', verify_ssl=verify_ssl)
    next_token = ''
    response = {}

    while True:
        if next_token == '':
            response = client.filter_log_events(
                logGroupName=log_group_name,
                startTime=int(start_time.timestamp() * 1000),
                endTime=int(end_time.timestamp() * 1000)
            )
        else:
            response = client.filter_log_events(
                logGroupName=log_group_name,
                startTime=int(start_time.timestamp() * 1000),
                endTime=int(end_time.timestamp() * 1000),
                nextToken=next_token
            )

        if 'nextToken' in response:
            next_token = response['nextToken']
            yield response['events']
        else:
            break


def save_to_csv(events, filename):
    """
    取得したログをCSVファイルに保存します。

    Args:
        events (list): イベントデータのリスト。
        filename (str): 保存するCSVファイルの名前。
    """
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for event in events:
            timestamp = datetime.fromtimestamp(event['timestamp'] / 1000).isoformat()
            message = json.loads(event['message'])
            log = message['log']
            writer.writerow([timestamp, log])


def main():
    """
    メイン関数: 引数を解析し、指定された条件でログを取得してCSVに保存します。
    """
    parser = argparse.ArgumentParser(description="CloudWatchログを取得してCSVに保存します。")
    parser.add_argument("--log-group", required=True, help="CloudWatchロググループ名を指定します。")
    parser.add_argument("--profile", required=True, help="使用するAWSプロファイル名を指定します。")
    parser.add_argument("--start-time", required=True, help="取得開始日時を YYYY-MM-DDTHH:MM:SS 形式で指定します。")
    parser.add_argument("--end-time", required=True, help="取得終了日時を YYYY-MM-DDTHH:MM:SS 形式で指定します。")
    parser.add_argument("--no-verify-ssl", action='store_false', help="SSL証明書認証をスキップします。")

    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime('%Y%m%d%H%M%S')
    parser.add_argument("--output-file", default=f"output_{formatted_datetime}.csv", help="保存するCSVファイルの名前を指定します。")

    args = parser.parse_args()

    start_time = datetime.strptime(args.start_time, "%Y-%m-%dT%H:%M:%S")
    end_time = datetime.strptime(args.end_time, "%Y-%m-%dT%H:%M:%S")

    for event in get_events(args.log_group, start_time, end_time, args.profile, args.no_verify_ssl):
        save_to_csv(event, args.output_file)
    
    print(f"Logs have been saved to {args.output_file}")

if __name__ == '__main__':
    main()
