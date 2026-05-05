import boto3
ec2 = boto3.client('ec2', region_name = 'eu-north-1')

def delete_running_ec2_instances():
    response = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values':['running']}])
    # Extract IDs from the nested structure
    instances_id = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances_id.append(instance['InstanceId'])
            print(f"Instance ID: {instance['InstanceId']}")

    if instances_id:
        response = ec2.terminate_instances(InstanceIds=instances_id)
    else:
        print("No instances running.")


if __name__ == '__main__':
    delete_running_ec2_instances()