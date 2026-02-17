import boto3
import click
import time
import uuid

TAGS = [{'Key': 'CreatedBy', 'Value': 'platform-cli'}, {'Key': 'Owner', 'Value': 'yifat'}]
REGION = 'us-east-1'


def get_latest_ami(os_type):
    ssm = boto3.client('ssm', region_name=REGION)
    paths = {
        'linux': '/aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2',
        'ubuntu': '/aws/service/canonical/ubuntu/server/22.04/stable/current/amd64/hvm/ebs-gp2/ami-id'
    }
    try:
        res = ssm.get_parameter(Name=paths[os_type])
        return res['Parameter']['Value']
    except:
        return None


@click.group()
def cli():
    """Yifat's AWS Management CLI"""
    pass


@cli.command()
@click.option('--type', type=click.Choice(['t3.micro', 't2.small']), default='t3.micro')
@click.option('--os', type=click.Choice(['linux', 'ubuntu']), default='linux')
def create_ec2(type, os):
    ec2 = boto3.client('ec2', region_name=REGION)
    ami_id = get_latest_ami(os)
    if not ami_id: return

    running = ec2.describe_instances(Filters=[
        {'Name': 'tag:CreatedBy', 'Values': ['platform-cli']},
        {'Name': 'instance-state-name', 'Values': ['running']}
    ])
    count = sum(len(r['Instances']) for r in running['Reservations'])
    if count >= 2:
        click.secho(f"✘ Error: Limit of 2 instances reached.", fg='red', bold=True)
        return

    ec2.run_instances(ImageId=ami_id, InstanceType=type, MinCount=1, MaxCount=1,
                      TagSpecifications=[{'ResourceType': 'instance', 'Tags': TAGS}])
    click.secho(f"✔ Success: {os} instance created using AMI: {ami_id}", fg='green', bold=True)


@cli.command()
def list_ec2():
    ec2 = boto3.client('ec2', region_name=REGION)
    instances = ec2.describe_instances(Filters=[{'Name': 'tag:CreatedBy', 'Values': ['platform-cli']}])
    click.secho("\n--- CLI Managed Instances ---", fg='cyan', bold=True)
    for r in instances['Reservations']:
        for i in r['Instances']:
            click.echo(f"ID: {i['InstanceId']} | Status: {i['State']['Name']}")


@cli.command()
@click.argument('instance_id')
def stop_ec2(instance_id):
    ec2 = boto3.client('ec2', region_name=REGION)
    ec2.stop_instances(InstanceIds=[instance_id])
    click.secho(f"✔ Instance {instance_id} stopping...", fg='yellow')

@cli.command()
@click.argument('name')
@click.option('--public', is_flag=True)
def create_s3(name, public):
    if public and not click.confirm("Are you sure you want this bucket to be PUBLIC?"): return
    s3 = boto3.client('s3')
    s3.create_bucket(Bucket=name)
    s3.put_bucket_tagging(Bucket=name, Tagging={'TagSet': TAGS})
    click.secho(f"✔ Bucket {name} created!", fg='green')


@cli.command()
@click.argument('file_path')
@click.argument('bucket_name')
def upload_file(file_path, bucket_name):
    s3 = boto3.client('s3')
    with click.progressbar(length=1, label='Uploading...') as bar:
        s3.upload_file(file_path, bucket_name, file_path.split('/')[-1])
        bar.update(1)
    click.secho(f"✔ File uploaded to {bucket_name}!", fg='green')


@cli.command()
def list_s3():
    s3 = boto3.client('s3')
    click.secho("\n--- CLI Managed Buckets ---", fg='cyan', bold=True)
    for b in s3.list_buckets()['Buckets']:
        try:
            tags = s3.get_bucket_tagging(Bucket=b['Name'])['TagSet']
            if any(t['Value'] == 'platform-cli' for t in tags):
                click.secho(f"Name: {b['Name']}", fg='green')
        except:
            continue


@cli.command()
@click.argument('domain')
def create_zone(domain):
    r53 = boto3.client('route53')
    res = r53.create_hosted_zone(Name=domain, CallerReference=str(uuid.uuid4()))
    z_id = res['HostedZone']['Id'].split('/')[-1]
    r53.change_tags_for_resource(ResourceType='hostedzone', ResourceId=z_id, AddTags=TAGS)
    click.secho(f"✔ Zone {domain} created!", fg='green')


@cli.command()
def list_zones():
    r53 = boto3.client('route53')
    click.secho("\n--- CLI Managed DNS ---", fg='cyan', bold=True)
    for z in r53.list_hosted_zones()['HostedZones']:
        z_id = z['Id'].split('/')[-1]
        try:
            tags = r53.list_tags_for_resource(ResourceType='hostedzone', ResourceId=z_id)['ResourceTagSet']['Tags']
            if any(t['Value'] == 'platform-cli' for t in tags):
                print(f"Domain: {z['Name']}")
        except:
            continue


if __name__ == '__main__':

    cli()
