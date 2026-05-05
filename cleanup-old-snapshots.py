import boto3
ec2 = boto3.client('ec2', region_name = 'eu-north-1')

def clean_up_old_snapshot():
    response = ec2.describe_volumes()
    volumes_id = []
    for volume in response['Volumes']:
        volumes_id.append(volume['VolumeId'])
    print('Volume Id: '+'\nVolume Id: '.join(volumes_id))
    for volume in volumes_id:
        response = ec2.describe_snapshots(
            OwnerIds=['self'],
            Filters = [{
                'Name': 'volume-id',
                'Values': [volume]
            }]
        )
        snap_list = response['Snapshots']
        sorted_snaps = sorted(snap_list, key=lambda x: x['StartTime'], reverse= True)
        # Keep the last 2 snapshots
        for snap in sorted_snaps[2:]:
            response = ec2.delete_snapshot(
                SnapshotId = snap['SnapshotId']
            )
            print(response)
            print(f"{snap['SnapshotId']} deleted.")


if __name__ == '__main__':
    clean_up_old_snapshot()