import json
from decimal import Decimal

from botobuddy.common import get_lambda_client


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


def response(data_or_error=None, rc=200, cors_origin='*'):
    """Returns a standardized response object for AWS Lambda with security headers.

    Args:
        data_or_error: The data to return in the response body or error message.
        rc: The HTTP status code to return. Defaults to 200.
        cors_origin: The allowed CORS origin. Defaults to '*' but should be restricted in production.

    Returns:
        A dictionary containing statusCode, headers, and body formatted for API Gateway.
    """
    if rc != 200:
        payload = {'IsSuccessful': False, 'Error': data_or_error}
    else:
        payload = {'IsSuccessful': True}

        if data_or_error:
            payload.update(data_or_error)

    return {
        'statusCode': rc,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type,Authorization,X-Amz-Date,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Origin': cors_origin,
            'Access-Control-Allow-Methods': 'OPTIONS,GET,POST,PUT,DELETE',
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
            'Content-Security-Policy': "default-src 'none'",
            'Cache-Control': 'no-store',
            'Content-Type': 'application/json; charset=utf-8',
        },
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

    pathParams = event.get('pathParameters')
    if pathParams:
        params.update(pathParams)

    qsParams = event.get('queryStringParameters')
    if qsParams:
        params.update(qsParams)

    if method == 'POST' or method == 'PUT':
        if 'body' not in event or not event['body']:
            raise UserWarning('A request body must be present for POST and PUT requests')

        try:
            params.update(json.loads(event['body']))
        except (json.JSONDecodeError, TypeError) as e:
            raise UserWarning('Invalid JSON payload in request body') from e

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


def get_function_url(function_name, session_config=None):
    """Get the configured URL for a Lambda function.

    Args:
        function_name: Name of the Lambda function.
        session_config: Configuration for the AWS session.

    Returns:
        The Function URL.

    Raises:
        ValueError: If the function URL configuration is not found.
    """
    if session_config is None:
        session_config = {}

    client = get_lambda_client(session_config)
    try:
        response = client.get_function_url_config(FunctionName=function_name)

        url = response['FunctionUrl']
        return url

    except client.exceptions.ResourceNotFoundException as e:
        raise ValueError(
            f'Function URL config for {function_name} not found. Ensure it is deployed with a Function URL.'
        ) from e
