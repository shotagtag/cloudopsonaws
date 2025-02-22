# CloudWatch AgentをEC2インスタンスにインストールしてみよう🚀

EC2インスタンスの詳細なメトリクスを取得したい場合には、CloudWatchエージェントを利用できます。
エージェントは常駐プログラムとして動作し、OS 内部から取得できる情報をメトリクスとして pushしたり、指定されたログファイルを CloudWatch Logs サービスに転送したりできます。
ラボ1の環境を流用し、EC2インスタンスにCloudWatchエージェントをインストールしてみましょう。

### 1.EC2インスタンスにCWエージェントをインストール、コンフィグファイルを作成

1. いずれかのEC2インスタンスにセッションマネージャーでログインします。
2. rootユーザーに切り替えます。
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

Trying to fetch the default region based on ec2 metadata...
I! imds retry client will retry 1 timesAre you using EC2 or On-Premises hosts?
1. EC2
2. On-Premises
default choice: [1]:
    <--- enterキーを入力(デフォルトを適用) # EC2
Which user are you planning to run the agent?
1. cwagent
2. root
3. others
default choice: [1]:
2    <--- 2を入力 # エージェントプロセス実行ユーザーの指定(実行ユーザーのログ読み取り権限などに注意する)
Do you want to turn on StatsD daemon?
1. yes
2. no
default choice: [1]:
2    <--- 2を入力 # statsdを使用しカスタムメトリクスを取得するかどうか
Do you want to monitor metrics from CollectD? WARNING: CollectD must be installed or the Agent will fail to start
1. yes
2. no
default choice: [1]:
2    <--- 2を入力 # collectdを使用しカスタムメトリクスを取得するかどうか
Do you want to monitor any host metrics? e.g. CPU, memory, etc.
1. yes
2. no
default choice: [1]:
    <--- enterキーを入力(デフォルトを適用) # CPUやメモリなどのメトリクスを取得するかどうか
Do you want to monitor cpu metrics per core?
1. yes
2. no
default choice: [1]:
2    <--- 2を入力 # CPUコアごとにCPUメトリクスを取得するかどうか
Do you want to add ec2 dimensions (ImageId, InstanceId, InstanceType, AutoScalingGroupName) into all of your metrics if the info is available?
1. yes
2. no
default choice: [1]:
    <--- enterキーを入力(デフォルトを適用) # 全てのメトリクスに提示された追加ディメンションを付加するかどうか
Do you want to aggregate ec2 dimensions (InstanceId)?
1. yes
2. no
default choice: [1]:
    <--- enterキーを入力(デフォルトを適用) # 未調査
Would you like to collect your metrics at high resolution (sub-minute resolution)? This enables sub-minute resolution for all metrics, but you can customize for specific metrics in the output json file.
1. 1s
2. 10s
3. 30s
4. 60s
default choice: [4]:
    <--- enterキーを入力(デフォルトを適用) # メトリクス取得間隔の指定
Which default metrics config do you want?
1. Basic
2. Standard
3. Advanced
4. None
default choice: [1]:
3    <--- 3を入力 # 取得するメトリクスのセットを指定
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
    <--- enterキーを入力(デフォルトを適用)
Do you have any existing CloudWatch Log Agent (http://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AgentReference.html) configuration file to import for migration?
1. yes
2. no
default choice: [2]:
    <--- enterキーを入力(デフォルトを適用)
Do you want to monitor any log files?
1. yes
2. no
default choice: [1]:
2    <--- 2を入力
Do you want the CloudWatch agent to also retrieve X-ray traces?
1. yes
2. no
default choice: [1]:
2    <--- 2を入力
Existing config JSON identified and copied to:  /opt/aws/amazon-cloudwatch-agent/etc/backup-configs
Saved config file to /opt/aws/amazon-cloudwatch-agent/bin/config.json successfully.
Current config as follows:
{
        "agent": {
                "metrics_collection_interval": 60,
                "run_as_user": "cwagent"
        },
        "logs": {
                "logs_collected": {
                        "files": {
                                "collect_list": [
                                        {
                                                "file_path": "/var/log/messages",
                                                "log_group_class": "STANDARD",
                                                "log_group_name": "messages",
                                                "log_stream_name": "{instance_id}",
                                                "retention_in_days": -1
                                        }
                                ]
                        }
                }
        },
        "metrics": {
                "aggregation_dimensions": [
                        [
                                "InstanceId"
                        ]
                ],
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
Please check the above content of the config.
The config file is also located at /opt/aws/amazon-cloudwatch-agent/bin/config.json.
Edit it manually if needed.
Do you want to store the config in the SSM parameter store?
1. yes
2. no
default choice: [1]:
2    <--- 2を入力
Program exits now.
```
