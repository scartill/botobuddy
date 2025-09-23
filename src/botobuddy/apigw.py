from botobuddy.common import get_apigateway_client


def get_api_uri(api_name: str) -> str:
    client = get_apigateway_client()

    for api in client.get_rest_apis()['items']:
        if api['name'] != f'{api_name}':
            continue

        region = api['tags']['aws:cloudformation:stack-id'].split(':')[3]

        return f'https://{api['id']}.execute-api.{region}.amazonaws.com/{api['name']}'

    raise ValueError('No API found')
