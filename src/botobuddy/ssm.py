from typing import Optional

from botobuddy.common import get_ssm_client, SSMClient


def get_ssm_parameter(name, session_config={}, ssm_client: Optional[SSMClient] = None):
    """Retrieve a parameter value from AWS SSM Parameter Store.

    Args:
        name (str): The name of the parameter to retrieve.
        session_config (dict): Optional AWS session configuration.
        ssm_client (Optional[SSMClient]): An existing SSM client to use.
            If not provided, a new one will be created.

    Returns:
        str: The value of the SSM parameter.
    """
    ssm = ssm_client or get_ssm_client(session_config)
    value = ssm.get_parameter(Name=name)['Parameter']['Value']
    return value
