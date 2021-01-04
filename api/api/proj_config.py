import os

def get_config():
    config = {
    ### Django Settings
    'allowed_hosts' : ['localhost', '127.0.0.1'],
    "cors_whitelist" : ['http://localhost:8080'],

    ### AWS
    'ssh_username' : 'ec2-user',
    'ec2_install_path' : '/home/ec2-user/server/',

    ### System
    'password' : 'password'
    }

    config['aws_access_key_id'] = os.environ['AWS_ACCESS_KEY']
    config['aws_secret_access_key'] = os.environ['AWS_SECRET']
    config['ssh_private_key_path'] = os.environ['SSH_PRIVATE_PATH']

    return config