import boto3
import schedule

client = boto3.client('eks', region_name='eu-north-1')

def get_all_clusters():
    clusters = []
    response = client.list_clusters()

    clusters.extend(response['clusters'])

    while 'nextToken' in response:
        response = client.list_clusters(nextToken=response['nextToken'])
        clusters.extend(response['clusters'])

    return clusters

def check_status_eks():
    clusters = get_all_clusters()

    if clusters :
        for cluster in clusters:
            response = client.describe_cluster(name=cluster)
            cluster_info = response['cluster']
            print(f"Name:    {cluster_info['name']}")
            print(f"Status:  {cluster_info['status']}")
            print(f"Version: {cluster_info['kubernetesVersion']}")
            print(f"ARN:     {cluster_info['arn']}")
            print("-" * 40)
    else:
        print("No clusters found.")


schedule.every(10).seconds.do(check_status_eks)

while True:
    schedule.run_pending()
