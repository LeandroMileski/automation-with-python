import boto3
import schedule

client = boto3.client('ec2', region_name = "eu-north-1")

def check_instance_status():
    response = client.describe_instance_status(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    if response:
        print("Status   ID")
        for inst in response['InstanceStatuses']:
            print(f"{inst['InstanceState']['Name']} {inst['InstanceId']}")
    print('----------')


schedule.every(5).seconds.do(check_instance_status)

while True:
    schedule.run_pending()

