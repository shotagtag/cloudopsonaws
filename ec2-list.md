### Python AWS SDK で EC2 インスタンスをリストする ###
SSM session manager で EC2インスタンスにログインし、以下のコマンドを実行します。
```
cd ~
aws configure set default.region ap-northeast-1
pip3 install boto3
sudo yum install -y git
git clone https://github.com/shotagtag/cloudopsonaws.git
cd cloudopsonaws
python3 ec2-list.py
```
