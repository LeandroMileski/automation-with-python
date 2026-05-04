import boto3

client = boto3.client('ec2', region_name = "eu-north-1")
instances_id = []

response = client.describe_instances(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        instances_id.append(instance['InstanceId'])

if instances_id:
    client.create_tags(
        Resources= instances_id,
        Tags=[
            {
                'Key': 'Env',
                'Value': 'dev'
            },
        ]
    )

print("Tagged:", instances_id)