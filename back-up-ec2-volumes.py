import schedule
import time
import boto3
ec2 = boto3.client('ec2', region_name = 'eu-north-1')

TAG_KEY = 'BACKUP'
TAG_VALUE = 'Yes'

def back_up_tagged_instances():
    response = ec2.describe_instances(
        Filters=[
            {'Name': f'tag:{TAG_KEY}', 'Values': [TAG_VALUE]},
            {'Name': 'instance-state-name', 'Values': ['running']}
        ])
    instances_id = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances_id.append(instance['InstanceId'])
    for instance_id in instances_id:
        response = ec2.create_snapshots(
            InstanceSpecification={
                'InstanceId': instance_id,
                'ExcludeBootVolume': False
            },
            Description= f'Automated full instance {instance_id} backup'
        )
        print(f'{instance_id} backup finished.')

# 🕒 Schedule (examples)
# schedule.every().day.at("02:00").do(back_up_tagged_instances)
schedule.every(5).minutes.do(back_up_tagged_instances)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)