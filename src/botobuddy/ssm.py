from typing import Optional

from botobuddy.common import get_ssm_client, SSMClient


def get_ssm_parameter(name, session_config={}, ssm_client: Optional[SSMClient] = None):
    """
    Get a parameter from AWS SSM Parameter Store

    Args:
        name: Name of the parameter.
        session_config: Session configuration.
        ssm_client: SSM client. No new client created if passed

    Returns:
        Parameter value.
    """
    ssm = ssm_client or get_ssm_client(session_config)
    value = ssm.get_parameter(Name=name)['Parameter']['Value']
    return value
