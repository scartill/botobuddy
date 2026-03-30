from typing import cast
from types_boto3_cloudformation import CloudFormationClient

from botobuddy.common import get_aws_client


def get_cloudformation_client(session_config: dict | None = None, profile: str | None = None) -> CloudFormationClient:
    """Get a CloudFormation client.

    Args:
        session_config (dict): Optional AWS session configuration.
        profile: Explicit AWS profile name. Takes precedence over session_config['profile'].

    Returns:
        CloudFormationClient: A Boto3 CloudFormation client.
    """
    if session_config is None:
        session_config = {}
    return cast(CloudFormationClient, get_aws_client('cloudformation', session_config, profile=profile))
