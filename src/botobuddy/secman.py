from typing import Optional
import json

from botobuddy.common import get_secretsmanager_client, SecretsManagerClient


def get_sm_secret(name, plain=False, session_config={}, sm_client: Optional[SecretsManagerClient] = None):
    """
    Get a secret from AWS Secrets Manager

    Args:
        name: Name of the secret.
        plain: Whether to return the secret as a plain string.
        session_config: Session configuration.
        sm_client: Secrets Manager client. No new client created if passed

    Returns:
        Secret value.
    """
    sm = sm_client or get_secretsmanager_client(session_config)
    get_secret_value_response = sm.get_secret_value(SecretId=name)
    secret_string = get_secret_value_response['SecretString']

    if plain:
        return secret_string
    else:
        return json.loads(secret_string)
