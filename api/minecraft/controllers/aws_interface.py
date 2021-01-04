import time
import os
import json

import boto3
import botocore
import paramiko

from django.conf import settings


from botocore.exceptions import ClientError

CONFIG = settings.CONFIG
SERVERS = settings.SERVERS

def load_server(name):
    if name not in SERVERS:
        return {}
    return SERVERS[name]

def startServer(server_name, dryRun=False):
    server = load_server(server_name)
    if not server:
        return {"ServerNotFound": True}

    inf = {"server": server_name}

    ec2 = boto3.client( 'ec2',
        aws_access_key_id = CONFIG['aws_access_key_id'],
        aws_secret_access_key = CONFIG['aws_secret_access_key'],
        region_name = server["aws_region"] )

    try:
        ec2.run_instances( MinCount = 1, MaxCount = 1,
            LaunchTemplate={
                'LaunchTemplateId': server["launchTemplateId"],
                'Version': server["launchTemplateVersion"]
            },
            DryRun = True )

    except ClientError as e:
        if 'DryRunOperation' not in str( e ):
            raise
    if dryRun:
        inf['publicIp'] = "Success"
        inf['publicDns'] = "Success"
        inf['instanceId'] = "Success"
        return inf

    try:
        response = ec2.run_instances( MinCount = 1, MaxCount = 1,
        LaunchTemplate={
            'LaunchTemplateId': server["launchTemplateId"],
            'Version': server["launchTemplateVersion"]
        },
        DryRun = False )
    except ClientError as e:
        print( e )

    time.sleep( 10.0 )

    inf['instanceId'] = response['Instances'][0]['InstanceId']

    ec2_resource = boto3.resource( 'ec2',
        aws_access_key_id = CONFIG['aws_access_key_id'],
        aws_secret_access_key = CONFIG['aws_secret_access_key'],
        region_name = server['aws_region'] )

    instance = ec2_resource.Instance( inf['instanceId'] )
    
    inf['publicIp'] = instance.public_ip_address
    inf['publicDns'] = instance.public_dns_name
    
    return inf


def stopServer( inf ):
    key = paramiko.RSAKey.from_private_key_file( CONFIG['ssh_private_key_path'] )
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy( paramiko.AutoAddPolicy() )

    # Connect/ssh to an instance
    try:
        # Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2
        client.connect( hostname=inf['publicDns'], username=CONFIG['ssh_username'], pkey=key )

        # Execute a command( cmd ) after connecting/ssh to an instance
        stdin, stdout, stderr = client.exec_command( 'nohup bash /home/ec2-user/shutdown.sh &>/dev/null &' )

        stdout.channel.recv_exit_status()
        # close the client connection once the job is done
        client.close()

    except Exception as e:
        print( e )

def getServerList():
    server_list = []
    for server in SERVERS:
        server_list.append({"key" : server,
                            "name": SERVERS[server]["name"]})
    return server_list