from typing import cast, Optional
from types_boto3_apigateway import APIGatewayClient

from botobuddy.common import get_aws_client


def get_apigateway_client(session_config: dict | None = None, profile: str | None = None) -> APIGatewayClient:
    """Get an API Gateway client.

    Args:
        session_config (dict): Optional AWS session configuration.
        profile: Explicit AWS profile name. Takes precedence over session_config['profile'].

    Returns:
        APIGatewayClient: A Boto3 API Gateway client.
    """
    if session_config is None:
        session_config = {}
    return cast(APIGatewayClient, get_aws_client('apigateway', session_config, profile=profile))


def get_api_uri(api_name: str, session_config: Optional[dict] = None, profile: str | None = None) -> str:
    """Get the URI for an API Gateway REST API.

    Args:
        api_name: The name of the API Gateway.
        session_config: Configuration for the AWS session.
        profile: Explicit AWS profile name. Takes precedence over session_config['profile'].

    Returns:
        The URI of the API Gateway.

    Raises:
        ValueError: If no API with the given name is found.
    """
    if session_config is None:
        session_config = {}
    client = get_apigateway_client(session_config, profile=profile)
    region = client.meta.region_name
    paginator = client.get_paginator('get_rest_apis')

    for page in paginator.paginate():
        for api in page.get('items', []):
            if api['name'] == api_name:
                return f"https://{api['id']}.execute-api.{region}.amazonaws.com"

    raise ValueError('No API found')
