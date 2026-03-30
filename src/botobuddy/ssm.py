from typing import cast, Optional
from types_boto3_ssm import SSMClient

from botobuddy.common import get_aws_client


def get_ssm_client(session_config: dict | None = None, profile: str | None = None) -> SSMClient:
    """Get an SSM client.

    Args:
        session_config (dict): Optional AWS session configuration.
        profile: Explicit AWS profile name. Takes precedence over session_config['profile'].

    Returns:
        SSMClient: A Boto3 SSM client.
    """
    if session_config is None:
        session_config = {}
    return cast(SSMClient, get_aws_client('ssm', session_config, profile=profile))


def get_ssm_parameter(name, session_config: dict | None = None, profile: str | None = None, ssm_client: Optional[SSMClient] = None):
    """Retrieve a parameter value from AWS SSM Parameter Store.

    Args:
        name (str): The name of the parameter to retrieve.
        session_config (dict): Optional AWS session configuration.
        profile: Explicit AWS profile name. Takes precedence over session_config['profile'].
        ssm_client (Optional[SSMClient]): An existing SSM client to use.
            If not provided, a new one will be created.

    Returns:
        str: The value of the SSM parameter.
    """
    if session_config is None:
        session_config = {}

    ssm = ssm_client or get_ssm_client(session_config, profile=profile)
    value = ssm.get_parameter(Name=name)['Parameter']['Value']
    return value
