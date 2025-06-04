import boto3


def get_aws_client(service, obj, resource=False):
    '''Create and return an AWS client with optional profile and region'''
    profile = obj.get('profile')
    region = obj.get('region')

    params = {}

    if profile:
        params['profile_name'] = profile

    if region:
        params['region_name'] = region

    session = boto3.Session(**params)

    if resource:
        return session.resource(service)
    else:
        return session.client(service)
