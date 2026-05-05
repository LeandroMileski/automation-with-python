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