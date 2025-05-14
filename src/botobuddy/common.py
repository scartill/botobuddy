import boto3


def get_aws_client(service, obj, resource=False):
    '''Create and return an AWS client with optional profile and region'''
    profile = obj.get('profile')
    region = obj.get('region')
    session = boto3.Session(profile_name=profile) if profile else boto3.Session()
    params = {'service': service}

    if region:
        params['region_name'] = region

    if resource:
        return session.resource(**params)
    else:
        return session.client(**params)
