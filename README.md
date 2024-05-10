# CloudWatch Logs Downloader

このPythonスクリプトは、指定された期間のAWS CloudWatchログを取得し、CSVファイルにエクスポートするために使用されます。ユーザーはコマンドラインから直接ロググループ名、AWSプロファイル、期間を指定することで、簡単にログデータを抽出できます。

## 前提条件
このスクリプトを使用する前に、以下の要件を満たしていることを確認してください：

- Python 3.6 以上がインストールされていること。
- boto3 ライブラリがインストールされていること。
- AWSの認証情報が設定されていること（.aws/credentialsおよび.aws/configファイルを通じて、または環境変数を設定して）。

## インストール方法
1. このリポジトリをクローンします。

2. 必要なPythonライブラリをインストールします：

```sh 
$ pip install -r requirements.txt
```

## 使用方法
スクリプトはコマンドラインから実行され、以下の引数を必要とします：

- --log-group: ログを取得するCloudWatchロググループの名前。
- --profile: 使用するAWSプロファイルの名前。
- --start-time ログ取得の開始日時（YYYY-MM-DDTHH:MM:SS形式）。
- --end-time: ログ取得の終了日時（YYYY-MM-DDTHH:MM:SS形式）。
- --output-file (オプション): 出力されるCSVファイルの名前（デフォルトはoutput_yyyyMMddHHmmss.csv）。
- --no-verify-ssl (オプション): SSL証明書認証をスキップします。

例えば、以下のコマンドでスクリプトを実行できます：

```sh
$ python download_cloudwatch_logs.py \
    --log-group "/aws/lambda/exampleLogGroup" \
    --profile "default" \
    --start-time "2023-01-01T00:00:00" \
    --end-time "2023-01-01T23:59:59" \
    --output-file "example_logs.csv" \
    --no-verify-ssl
```
