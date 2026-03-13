from typing import Optional
import json

from botobuddy.common import get_secretsmanager_client, SecretsManagerClient


def get_sm_secret(name, plain=False, session_config={}, sm_client: Optional[SecretsManagerClient] = None):
    """Retrieve a secret from AWS Secrets Manager.

    Args:
        name (str): The name of the secret to retrieve.
        plain (bool): If True, returns the raw secret string. If False (default), 
            returns the JSON-parsed secret.
        session_config (dict): Optional AWS session configuration.
        sm_client (Optional[SecretsManagerClient]): An existing Secrets Manager 
            client to use. If not provided, a new one will be created.

    Returns:
        Union[dict, str]: The secret value, either as a dictionary or a string.
    """
    sm = sm_client or get_secretsmanager_client(session_config)
    get_secret_value_response = sm.get_secret_value(SecretId=name)
    secret_string = get_secret_value_response['SecretString']

    if plain:
        return secret_string
    else:
        return json.loads(secret_string)
