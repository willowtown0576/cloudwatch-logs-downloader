# CloudWatch Logs Downloader

このPythonスクリプトは、指定された期間のAWS CloudWatchログを取得し、CSVファイルにエクスポートするために使用されます。ユーザーはコマンドラインから直接ロググループ名、AWSプロファイル、期間を指定することで、簡単にログデータを抽出できます。

## 前提条件
このスクリプトを使用する前に、以下の要件を満たしていることを確認してください：

- Python 3.6 以上がインストールされていること。
- boto3 ライブラリがインストールされていること。
- AWSの認証情報が設定されていること（.aws/credentialsおよび.aws/configファイルを通じて、または環境変数を設定して）。

## インストール方法
1. 必要なPythonライブラリをインストールします：

```bash 
$ pip install boto3
```

2. このリポジトリをクローンするか、スクリプトファイルをダウンロードします。

## 使用方法
スクリプトはコマンドラインから実行され、以下の引数を必要とします：

- --log-group: ログを取得するCloudWatchロググループの名前。
- --profile: 使用するAWSプロファイルの名前。
- --start_date: ログ取得の開始日時（YYYY-MM-DDTHH:MM:SS形式）。
- --end_date: ログ取得の終了日時（YYYY-MM-DDTHH:MM:SS形式）。
- --output_file (オプション): 出力されるCSVファイルの名前（デフォルトはoutput.csv）。
- --limit (オプション): 取得するログの最大数（デフォルトは10000件）。
- --no-limit (オプション): ログの取得数に上限を設定しない場合に指定。

例えば、以下のコマンドでスクリプトを実行できます：

```bash
$ python download_cloudwatch_logs.py \
    --log-group "/aws/lambda/exampleLogGroup" \
    --profile "default" \
    --start_date "2023-01-01T00:00:00" \
    --end_date "2023-01-01T23:59:59" \
    --output_file "example_logs.csv"
```
