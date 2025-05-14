import boto3


def get_aws_client(service, region=None, profile=None):
    '''Create and return an AWS client with optional profile and region'''
    session = boto3.Session(profile_name=profile) if profile else boto3.Session()
    return session.client(service, region_name=region) if region else session.client(service)
