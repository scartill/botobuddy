from botobuddy.common import get_apigateway_client
from typing import Optional


def get_api_uri(api_name: str, session_config: Optional[dict] = None) -> str:
    """Get the URI for an API Gateway REST API.

    Args:
        api_name: The name of the API Gateway.
        session_config: Configuration for the AWS session.

    Returns:
        The URI of the API Gateway.

    Raises:
        ValueError: If no API with the given name is found.
    """
    if session_config is None:
        session_config = {}
    client = get_apigateway_client(session_config)
    region = client.meta.region_name
    paginator = client.get_paginator('get_rest_apis')

    for page in paginator.paginate():
        for api in page.get('items', []):
            if api['name'] == api_name:
                return f"https://{api['id']}.execute-api.{region}.amazonaws.com"

    raise ValueError('No API found')
