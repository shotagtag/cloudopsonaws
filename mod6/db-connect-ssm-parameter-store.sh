## パラメータとコードを分離する
#!/bin/bash

# SSM パラメータストアから接続情報を取得
DB_HOST=$(aws ssm get-parameter --name "/mydatabase/host" --query "Parameter.Value" --output text)

DB_USER=$(aws ssm get-parameter --name "/mydatabase/user" --query "Parameter.Value" --output text)

DB_PASS=$(aws ssm get-parameter --name "/mydatabase/password" --with-decryption --query "Parameter.Value" --output text)

DB_NAME=$(aws ssm get-parameter --name "/mydatabase/database" --query "Parameter.Value" --output text)

# MySQLデータベース に接続
mysql -h $DB_HOST -u $DB_USER -p$DB_PASS $DB_NAME

# * 本来は "aws ssm get-parameters-by-path --path /mydatabase/ --with-decryption" のようにまとめてパラメータを取得したほう、API呼び出し回数の観点などから望ましい
