
import json
from decimal import Decimal


class DynamoFriendlyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj)

        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


def response(data_or_error=None, rc=200):
    if rc != 200:
        payload = {
            'IsSuccessful': False,
            'Error': data_or_error
        }
    else:
        payload = {'IsSuccessful': True}

        if data_or_error:
            payload.update(data_or_error)

    return {
        'statusCode': rc,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,GET,POST,PUT,DELETE'
        },
        'body': json.dumps(payload, cls=DynamoFriendlyEncoder)
    }


def request_params(event):
    params = dict()
    method = event['httpMethod']

    pathParams = event.get('pathParameters')
    if pathParams:
        params.update(pathParams)

    qsParams = event.get('queryStringParameters')
    if qsParams:
        params.update(qsParams)

    if method == 'POST' or method == 'PUT':
        if 'body' not in event:
            raise UserWarning(
                'A request body must be present for POST and PUT requests'
            )

        params.update(json.loads(event['body']))

    return (method, params)
