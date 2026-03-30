from typing import cast
from types_boto3_cognito_idp import CognitoIdentityProviderClient

from botobuddy.common import get_aws_client


def get_cognito_client(session_config: dict | None = None, profile: str | None = None) -> CognitoIdentityProviderClient:
    """Get a Cognito Identity Provider client.

    Args:
        session_config (dict): Optional AWS session configuration.
        profile: Explicit AWS profile name. Takes precedence over session_config['profile'].

    Returns:
        CognitoIdentityProviderClient: A Boto3 Cognito client.
    """
    if session_config is None:
        session_config = {}
    return cast(CognitoIdentityProviderClient, get_aws_client('cognito-idp', session_config, profile=profile))
