from typing import Any

import boto3
from botocore.config import Config

from botobuddy.logger import logger


def get_aws_session(session_config: dict | None = None, profile: str | None = None) -> boto3.Session:
    """Create and return an AWS session with optional profile and region

    Args:
        session_config: A dictionary of session configuration options:
        - profile: The AWS profile to use
        - region: The AWS region to use
        - assume_role: The AWS role ARN to assume
        - session_name: The name of the session
        profile: Explicit AWS profile name. Takes precedence over session_config['profile'].

    Returns:
        A boto3.Session object
    """
    if session_config is None:
        session_config = {}

    profile = profile or session_config.get('profile')
    region = session_config.get('region')

    params = {}

    if profile:
        logger.info(f'Using AWS profile: {profile}')
        params['profile_name'] = profile

    if region:
        logger.info(f'Using AWS region: {region}')
        params['region_name'] = region

    logger.info('Creating AWS session')
    session = boto3.Session(**params)

    if assume_role := session_config.get('assume_role'):
        session_name = session_config.get('session_name') or 'botobuddy-session'
        allowed_session_name_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_=,.@-')

        if not isinstance(session_name, str):
            raise ValueError('session_name must be a string')
        if len(session_name) > 64:
            raise ValueError('session_name must be 64 characters or fewer')
        if not session_name or any(char not in allowed_session_name_chars for char in session_name):
            raise ValueError(
                'session_name must be non-empty and contain only letters, numbers, and the characters _=,.@-'
            )
        sts_client = session.client('sts')

        assumed_role_object = sts_client.assume_role(RoleArn=assume_role, RoleSessionName=session_name)

        logger.info(f'Assumed role {assume_role} with session name {session_name}')

        # Log only the assumed role user details to avoid exposing sensitive credentials in debug logs
        assumed_role_user = assumed_role_object.get('AssumedRoleUser', {})
        logger.debug(f'Assumed role user: {assumed_role_user}')

        credentials = assumed_role_object['Credentials']

        assume_params = {
            'aws_access_key_id': credentials['AccessKeyId'],
            'aws_secret_access_key': credentials['SecretAccessKey'],
            'aws_session_token': credentials['SessionToken'],
        }

        if region:
            logger.info(f'Using AWS region: {region} for assumed role')
            assume_params['region_name'] = region

        logger.info('Creating AWS session with assumed role')
        session = boto3.Session(**assume_params)  # type: ignore

    return session


def get_aws_client(
    service: str,
    session_config: dict | None = None,
    profile: str | None = None,
    resource: bool = False,
    core_config: dict | None = None
) -> Any:
    """Create and return an AWS client or resource.

    Args:
        service: The AWS service name (e.g., 's3', 'dynamodb').
        session_config: Configuration for the AWS session.
        profile: Explicit AWS profile name. Takes precedence over session_config['profile'].
        resource: Whether to return a Boto3 resource instead of a client.
        core_config: Optional botocore configuration dictionary.

    Returns:
        An AWS client or resource object.
    """
    if session_config is None:
        session_config = {}

    session = get_aws_session(session_config, profile=profile)

    client_params = {'service_name': service}

    if core_config:
        logger.debug(f'Using core session config: {core_config}')
        botocore_config = Config(**core_config)
        client_params['config'] = botocore_config

    if resource:
        result = session.resource(**client_params)
    else:
        result = session.client(**client_params)

    return result

