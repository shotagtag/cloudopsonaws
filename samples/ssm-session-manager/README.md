### Systems Manager セッションマネージャーを使用してみる ###
- マネジメントコンソールで EC2 サービス画面を開きます。
- 左メニューより、「インスタンス」をクリックし、EC2 インスタンス一覧を表示します。
- 1 つのインスタンスのチェックボックスを選択します。インスタンスは SSH に必要なインバウンドのポート解放が行われていません。
- 画面上部の「接続」をクリックします。
- 「インスタンスに接続」画面で「セッションマネージャー」タブを選択し、「接続」をクリックします。
- プロンプトが表示されたら、ログイン成功です。

### EC2 インスタンスで AWS CLI, AWS SDK を使ってみる ###
- CLI, SDK で AWS にリクエストを発行する際のデフォルトで指定するリージョンを設定します。
```
cd ~
aws configure set default.region ap-northeast-1
```

- EC2 インスタンスをリストで情報取得する CLI コマンドを実行します。
```
aws ec2 describe-instances
```

- Python 用の AWSSDK (boto3) をインストールします。
  - 参考 : [Boto3 documentation — Boto3 Docs 1.26.65 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

```
pip3 install boto3
```
- EC2 インスタンスをリストするプログラムを取得します。 
```
sudo yum install -y git
git clone https://github.com/shotagtag/cloudopsonaws
cd cloudopsonaws/samples/ssm-session-manager/
```

- プログラムを実行します。EC2 インスタンスのインスタンス ID, 状態, インスタンスタイプ が表示されます。
```
python3 ec2-list.py
```
