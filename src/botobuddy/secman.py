
from functools import cache
import json

import boto3


@cache
def get_sm_secret(name, plain=False):
    sm = boto3.client('secretsmanager')
    get_secret_value_response = sm.get_secret_value(SecretId=name)
    secret_string = get_secret_value_response['SecretString']

    if plain:
        return secret_string
    else:
        return json.loads(secret_string)
