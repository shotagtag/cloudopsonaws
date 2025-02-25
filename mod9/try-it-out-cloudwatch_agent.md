# CloudWatch AgentをEC2インスタンスにインストールしてみよう🚀

EC2インスタンスはデフォルトで、CPU使用率やネットワーク流量などのCloudWatchメトリクスが取得されます。ただし、メモリ使用量やディスク使用率などOSレベルのメトリクスは提供されません。OSレベルの詳細なメトリクスを取得したい場合には、CloudWatchエージェントを利用できます。エージェントは常駐プログラムとして動作し、OS 内部から取得できる情報をメトリクスとして pushしたり、指定されたログファイルを CloudWatch Logs サービスに転送したりできます。
ラボ1の環境を流用し、EC2インスタンスにCloudWatchエージェントをインストールしてみましょう。

### 1.EC2インスタンスにCWエージェントをインストール、コンフィグファイルを作成

1. いずれかのEC2インスタンス(Web Server または App Server)にセッションマネージャーでログインします。
![image](https://github.com/user-attachments/assets/b95dddb7-9741-4b57-bfaa-58d74a3d42c3)

3. rootユーザーに切り替えます。
```
sudo su -
```
3. CloudWatchエージェントをインストールします。
```
yum install amazon-cloudwatch-agent -y
```
4. エージェントを起動するためにはコンフィグファイルが必要です。コンフィグファイルを生成するための補助ツールであるウィザードを起動しましょう。
```
/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-config-wizard
```

5. 起動したら次の出力を参考に質問に答えます。間違えたらctrl+cなどで中断し、4からやり直してください。
```
On which OS are you planning to use the agent?
1. linux
2. windows
3. darwin
default choice: [1]:
    <--- enterキーを入力(デフォルトを適用) # Linux,Windows,Macの選択
```
```
Trying to fetch the default region based on ec2 metadata...
I! imds retry client will retry 1 timesAre you using EC2 or On-Premises hosts?
1. EC2
2. On-Premises
default choice: [1]:
    <--- enterキーを入力(デフォルトを適用) # 監視対象のEC2インスタンス or オンプレサーバーどちらか
```
```
Which user are you planning to run the agent?
1. cwagent
2. root
3. others
default choice: [1]:
    <--- enterキーを入力(デフォルトを適用) # エージェントプロセス実行ユーザーの指定(ログを送信する場合読み取り権限に注意する)
```
```
Do you want to turn on StatsD daemon?
1. yes
2. no
default choice: [1]:
2    <--- 2を入力 # statsdと連携し、より発展的なカスタムメトリクスを取得するかどうか
```
```
Do you want to monitor metrics from CollectD? WARNING: CollectD must be installed or the Agent will fail to start
1. yes
2. no
default choice: [1]:
2    <--- 2を入力 # collectdと連携し、より発展的なカスタムメトリクスを取得するかどうか
```
```
Do you want to monitor any host metrics? e.g. CPU, memory, etc.
1. yes
2. no
default choice: [1]:
    <--- enterキーを入力(デフォルトを適用) # CPUやメモリなどのホスト詳細メトリクスを取得するかどうか
```
```
Do you want to monitor cpu metrics per core?
1. yes
2. no
default choice: [1]:
    <--- enterキーを入力(デフォルトを適用) # CPUコアごとにCPUメトリクスを取得するかどうか
```
```
Do you want to add ec2 dimensions (ImageId, InstanceId, InstanceType, AutoScalingGroupName) into all of your metrics if the info is available?
1. yes
2. no
default choice: [1]:
    <--- enterキーを入力(デフォルトを適用) # 全てのメトリクスに、提示された追加ディメンションが付加できる場合付与するかどうか
```
```
Do you want to aggregate ec2 dimensions (InstanceId)?
1. yes
2. no
default choice: [1]:
    <--- enterキーを入力(デフォルトを適用)
```
```
Would you like to collect your metrics at high resolution (sub-minute resolution)? This enables sub-minute resolution for all metrics, but you can customize for specific metrics in the output json file.
1. 1s
2. 10s
3. 30s
4. 60s
default choice: [4]:
    <--- enterキーを入力(デフォルトを適用) # メトリクス取得間隔の指定
```
```
Which default metrics config do you want?
1. Basic
2. Standard
3. Advanced
4. None
default choice: [1]:
3    <--- 3を入力 # どの(レベルの)既定のメトリクスセット設定がよいか指定
```
```
Current config as follows:
{
        "agent": {
                "metrics_collection_interval": 60,
                "run_as_user": "cwagent"
        },
        "metrics": {
                "aggregation_dimensions": [
                        [
                                "InstanceId"
                        ]
                ],
                "append_dimensions": {
                        "AutoScalingGroupName": "${aws:AutoScalingGroupName}",
                        "ImageId": "${aws:ImageId}",
                        "InstanceId": "${aws:InstanceId}",
                        "InstanceType": "${aws:InstanceType}"
                },
                "metrics_collected": {
                        "cpu": {
                                "measurement": [
                                        "cpu_usage_idle",
                                        "cpu_usage_iowait",
                                        "cpu_usage_user",
                                        "cpu_usage_system"
                                ],
                                "metrics_collection_interval": 60,
                                "resources": [
                                        "*"
                                ],
                                "totalcpu": false
                        },
                        "disk": {
                                "measurement": [
                                        "used_percent",
                                        "inodes_free"
                                ],
                                "metrics_collection_interval": 60,
                                "resources": [
                                        "*"
                                ]
                        },
                        "diskio": {
                                "measurement": [
                                        "io_time",
                                        "write_bytes",
                                        "read_bytes",
                                        "writes",
                                        "reads"
                                ],
                                "metrics_collection_interval": 60,
                                "resources": [
                                        "*"
                                ]
                        },
                        "mem": {
                                "measurement": [
                                        "mem_used_percent"
                                ],
                                "metrics_collection_interval": 60
                        },
                        "netstat": {
                                "measurement": [
                                        "tcp_established",
                                        "tcp_time_wait"
                                ],
                                "metrics_collection_interval": 60
                        },
                        "swap": {
                                "measurement": [
                                        "swap_used_percent"
                                ],
                                "metrics_collection_interval": 60
                        }
                }
        }
}
Are you satisfied with the above config? Note: it can be manually customized after the wizard completes to add additional items.
1. yes
2. no
default choice: [1]:
    <--- enterキーを入力(デフォルトを適用) # このコンフィグ内容で良いかの確認
```
```
Do you have any existing CloudWatch Log Agent (http://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AgentReference.html) configuration file to import for migration?
1. yes
2. no
default choice: [2]:
    <--- enterキーを入力(デフォルトを適用) # 既存のCloudWatch Logs Agent(旧ツール)があり、マイグレーションしたいか？
```
```
Do you want to monitor any log files?
1. yes
2. no
default choice: [1]:
2    <--- 2を入力 # CloudWatch Logsに送りたいログはあるか
```
```
Do you want the CloudWatch agent to also retrieve X-ray traces?
1. yes
2. no
default choice: [1]:
2    <--- 2を入力 # AWS X-Ray トレース情報を取得する役割も有効化するか？
```
```
xisting config JSON identified and copied to:  /opt/aws/amazon-cloudwatch-agent/etc/backup-configs
Saved config file to /opt/aws/amazon-cloudwatch-agent/bin/config.json successfully.
Current config as follows:

<json表示中略>

Do you want to store the config in the SSM parameter store?
1. yes
2. no
default choice: [1]:
2    <--- 2を入力 # Systems Manager パラメータストアにコンフィグを保管するか？
Program exits now.
```

6. ローカルに生成されたコンフィグファイルを確認します。
```
cat /opt/aws/amazon-cloudwatch-agent/bin/config.json
```

7. コンフィグファイルを基に CLoudWatchエージェントを起動します。
```
/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -s -c file:/opt/aws/amazon-cloudwatch-agent/bin/config.json
```
★コマンドの意味参考
- `-a fetch-config` : アクション（-a）として "fetch-config" を指定しています。これは設定ファイルを取得し、適用することを意味します。
- `-m ec2` : モード（-m）として "ec2" を指定しています。エージェントが EC2 インスタンス上で動作していることを示します。
- `-s` : コンフィグファイルの再読み込みや追加などを行った場合、ついでにエージェントを再起動するかどうかのオプションです。
- `-c file:/opt/aws/amazon-cloudwatch-agent/bin/config.json` : 設定ファイル（-c）のパスを指定しています。この場合、ローカルファイルシステム上の JSON 設定ファイルを使用します。他にssmパラメータストア(ssm:)やトライアル用のコンフィグ(default)を指定することもできます。

8. エージェントが起動しているか確認します。
- `Active: active (running)`の表示があれば起動しています
```
systemctl status amazon-cloudwatch-agent.service
```

9. マネジメントコンソールで CloudWatch を開きます。
11. 左ナビゲーションペインから、**すべてのメトリクス** を選択します。
![image](https://github.com/user-attachments/assets/646d3b9e-743a-44dc-babb-44d3cd2b7bf0)

13. `CWAgent`の名前空間をクリックし、メトリクスが収集されているか確認します。
![image](https://github.com/user-attachments/assets/35a5595b-4b54-43e9-a34a-05b41756d92a)
