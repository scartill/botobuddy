from typing import Optional
import json

from typing import cast, Optional
from types_boto3_secretsmanager import SecretsManagerClient

from botobuddy.common import get_aws_client


def get_secretsmanager_client(session_config: dict | None = None, profile: str | None = None) -> SecretsManagerClient:
    """Get a Secrets Manager client.

    Args:
        session_config (dict): Optional AWS session configuration.
        profile: Explicit AWS profile name. Takes precedence over session_config['profile'].

    Returns:
        SecretsManagerClient: A Boto3 Secrets Manager client.
    """
    if session_config is None:
        session_config = {}
    return cast(SecretsManagerClient, get_aws_client('secretsmanager', session_config, profile=profile))


def get_sm_secret(name, plain: bool = False, session_config=None, profile: str | None = None, sm_client: Optional[SecretsManagerClient] = None):
    """Retrieve a secret from AWS Secrets Manager.

    Args:
        name (str): The name of the secret to retrieve.
        plain (bool): If True, returns the raw secret string. If False (default), 
            returns the JSON-parsed secret.
        session_config (dict): Optional AWS session configuration.
        profile: Explicit AWS profile name. Takes precedence over session_config['profile'].
        sm_client (Optional[SecretsManagerClient]): An existing Secrets Manager 
            client to use. If not provided, a new one will be created.

    Returns:
        Union[dict, str]: The secret value, either as a dictionary or a string.
    """
    if session_config is None:
        session_config = {}

    sm = sm_client or get_secretsmanager_client(session_config, profile=profile)
    get_secret_value_response = sm.get_secret_value(SecretId=name)
    secret_string = get_secret_value_response['SecretString']

    if plain:
        return secret_string
    else:
        return json.loads(secret_string)
