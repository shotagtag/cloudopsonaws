import boto3

# EC2クライアントの作成
ec2 = boto3.client('ec2')

# インスタンスの情報を取得
response = ec2.describe_instances()

# インスタンスのリストを表示
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        instance_id = instance['InstanceId']
        state = instance['State']['Name']
        instance_type = instance['InstanceType']
        print(f"Instance ID: {instance_id}, State: {state}, Instance Type: {instance_type}")
