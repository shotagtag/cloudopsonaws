import base64
import json
import zlib
import datetime
import os
import boto3
from botocore.exceptions import ClientError

print('Loading function')

def lambda_handler(event, context):
    data = zlib.decompress(base64.b64decode(event['awslogs']['data']), 16+zlib.MAX_WBITS)
    data_json = json.loads(data)
    log_group = data_json['logGroup']
    log_stream = data_json['logStream']
    log_owner = data_json['owner']
    log_entire_json = json.loads(json.dumps(data_json["logEvents"], ensure_ascii=False))
    log_entire_len = len(log_entire_json)

    print(data_json)

    for i in range(log_entire_len): 
        log_json = json.loads(json.dumps(data_json["logEvents"][i], ensure_ascii=False))
        
        # タイムスタンプをISO形式の日時文字列に変換
        timestamp = datetime.datetime.fromtimestamp(log_json['timestamp'] / 1000.0).isoformat()

        # メッセージを整形
        formatted_message = f"""
****
AWS アカウント : {log_owner}
Log Group はこちら : {log_group}
Log Stream はこちら : {log_stream}
Timestamp: {timestamp}
メッセージ : {log_json['message']}
****
        """

        try:
            sns = boto3.client('sns')
    
            #SNS Publish 要Lambda環境変数
            publishResponse = sns.publish(
                TopicArn = os.environ['SNS_TOPIC_ARN'],
                Message = formatted_message,
                Subject = os.environ['ALARM_SUBJECT']
            )
    
        except Exception as e:
            print(e)
