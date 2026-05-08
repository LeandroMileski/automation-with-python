import time

import boto3

client = boto3.client('ec2', region_name='eu-north-1')

response = client.run_instances(
    ImageId='ami-059f32cf6eecf0ef9',
    InstanceType='t3.micro',
    MinCount=1,
    MaxCount=1,
    # Optional: assign a Name tag during creation
    TagSpecifications=[{
        'ResourceType': 'instance',
        'Tags': [{'Key': 'BACKUP', 'Value': 'Yes'}]
    }]
)

instance_id = response['Instances'][0]['InstanceId']
print(f"Launched Instance ID: {instance_id}")

# Wait until the instance is in 'running' state and has a public IP
print("Waiting for instance to be running...")
waiter = client.get_waiter('instance_running')
waiter.wait(InstanceIds=[instance_id])

# Now fetch fresh instance data
instance_info = client.describe_instances(InstanceIds=[instance_id])
instance_ip = instance_info['Reservations'][0]['Instances'][0].get('PublicIpAddress')
print(f"Instance IP: {instance_ip}")