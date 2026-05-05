import json
from decimal import Decimal

from typing import cast
from types_boto3_lambda import LambdaClient

from botobuddy.common import get_aws_client
from botobuddy.logger import logger


def get_lambda_client(session_config: dict | None = None, profile: str | None = None) -> LambdaClient:
    """Get a Lambda client.

    Args:
        session_config (dict): Optional AWS session configuration.
        profile: Explicit AWS profile name. Takes precedence over session_config['profile'].

    Returns:
        LambdaClient: A Boto3 Lambda client.
    """
    if session_config is None:
        session_config = {}
    return cast(LambdaClient, get_aws_client('lambda', session_config, profile=profile))


class DynamoFriendlyEncoder(json.JSONEncoder):
    """A JSON encoder that converts Decimal objects to integers.

    This encoder is useful when working with DynamoDB data that contains Decimal types
    which are not JSON serializable by default.
    """

    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj)

        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


def response(data_or_error=None, rc=200, cors_origin='*', additional_headers=None):
    """Returns a standardized response object for AWS Lambda with security headers.

    Args:
        data_or_error: The data to return in the response body or error message.
        rc: The HTTP status code to return. Defaults to 200.
        cors_origin: The allowed CORS origin. Defaults to '*' but should be restricted in production.
        additional_headers: Optional dictionary of additional headers or overrides for default headers.

    Returns:
        A dictionary containing statusCode, headers, and body formatted for API Gateway.
    """
    if rc != 200:
        if isinstance(data_or_error, Exception):
            # SECURITY: Log actual exception details internally but mask them from the API response
            # to prevent leaking internal implementation details or stack traces to the client.
            logger.error('Operation failed', exc_info=data_or_error)
            error_msg = 'An internal server error occurred'
        else:
            error_msg = data_or_error
        payload = {'IsSuccessful': False, 'Error': error_msg}
    else:
        payload = {'IsSuccessful': True}

        if data_or_error:
            if isinstance(data_or_error, dict):
                payload.update(data_or_error)
            else:
                payload['Data'] = data_or_error

    headers = {
        'Access-Control-Allow-Headers': 'Content-Type,Authorization,X-Amz-Date,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Origin': cors_origin,
        'Access-Control-Allow-Methods': 'OPTIONS,GET,POST,PUT,DELETE',
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'Content-Security-Policy': "default-src 'none'",
        'Cache-Control': 'no-store'
    }

    if additional_headers:
        headers.update(additional_headers)

    return {
        'statusCode': rc,
        'headers': headers,
        'body': json.dumps(payload, cls=DynamoFriendlyEncoder),
    }


def request_params(event):
    """Returns the HTTP method and parameters of the current request.

    Extracts path parameters, query string parameters, and body (for POST/PUT).

    Args:
        event: The AWS Lambda event object.

    Returns:
        A tuple containing the HTTP method (str) and a dictionary of parameters.

    Raises:
        UserWarning: If a request body is missing for POST or PUT requests.

    Examples:
        ('GET', {'path': 'example'})
        ('POST', {'body': {'key': 'value'}})
        ('PUT', {'body': {'key': 'value'}})
        ('DELETE', {'path': 'example'})
        ('OPTIONS', {})
        ('PATCH', {'body': {'key': 'value'}})
        ('HEAD', {})
        ('TRACE', {})
    """
    params = dict()
    method = event['httpMethod']

    if method == 'POST' or method == 'PUT':
        if 'body' not in event or not event['body']:
            raise UserWarning('A request body must be present for POST and PUT requests')

        body = event['body']

        # Normalize body to bytes for size checking
        if isinstance(body, str):
            body_bytes = body.encode('utf-8')
        elif isinstance(body, bytes):
            body_bytes = body
        else:
            raise UserWarning('Unexpected request body type; expected text or bytes')

        # SECURITY: Limit request body length to 5MB (in bytes) to prevent DoS via memory exhaustion
        if len(body_bytes) > 5 * 1024 * 1024:
            raise UserWarning('Request body exceeds maximum allowed size (5MB)')

        try:
            # Decode as UTF-8 text for JSON parsing
            if isinstance(body, bytes):
                body_text = body_bytes.decode('utf-8')
            else:
                # body was str; reuse it to avoid double-decoding
                body_text = body
        except UnicodeDecodeError as e:
            raise UserWarning('Invalid encoding in request body; expected UTF-8 text') from e

        try:
            parsed_body = json.loads(body_text)
            if not isinstance(parsed_body, dict):
                raise UserWarning('JSON payload must be an object/dictionary')
            params.update(parsed_body)
        except json.JSONDecodeError as e:
            raise UserWarning('Invalid JSON payload in request body') from e

    qsParams = event.get('queryStringParameters')
    if qsParams:
        params.update(qsParams)

    pathParams = event.get('pathParameters')
    if pathParams:
        params.update(pathParams)

    return (method, params)


def get_this_url(event):
    """Returns the full URL of the current request.

    Args:
        event: The AWS Lambda event object.

    Returns:
        The full URL string including protocol, domain, and path.
    """
    requestContext = event['requestContext']
    domainName = requestContext['domainName']
    path = requestContext['path']
    return f'https://{domainName}{path}'


def get_function_url(function_name, session_config=None, profile: str | None = None):
    """Get the configured URL for a Lambda function.

    Args:
        function_name: Name of the Lambda function.
        session_config: Configuration for the AWS session.
        profile: Explicit AWS profile name. Takes precedence over session_config['profile'].

    Returns:
        The Function URL.

    Raises:
        ValueError: If the function URL configuration is not found.
    """
    if session_config is None:
        session_config = {}

    client = get_lambda_client(session_config, profile=profile)
    try:
        response = client.get_function_url_config(FunctionName=function_name)

        url = response['FunctionUrl']
        return url

    except client.exceptions.ResourceNotFoundException as e:
        raise ValueError(
            f'Function URL config for {function_name} not found. Ensure it is deployed with a Function URL.'
        ) from e
