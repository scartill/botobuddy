import logging as lg
from typing import cast

import randomname
import boto3
from types_boto3_s3 import S3Client
from types_boto3_dynamodb import DynamoDBClient, DynamoDBServiceResource
from types_boto3_route53 import Route53Client
from types_boto3_sts import STSClient


type AWSClient = S3Client | DynamoDBClient | DynamoDBServiceResource | Route53Client | STSClient


def get_aws_client(service, obj, resource=False) -> AWSClient:
    '''Create and return an AWS client with optional profile and region'''
    profile = obj.get('profile')
    region = obj.get('region')

    params = {}

    if profile:
        lg.info(f'Using AWS profile: {profile}')
        params['profile_name'] = profile

    if region:
        lg.info(f'Using AWS region: {region}')
        params['region_name'] = region

    lg.info('Creating AWS session')
    session = boto3.Session(**params)

    if assume_role := obj.get('assume_role'):
        session_name = randomname.get_name()
        sts_client = session.client('sts')

        assumed_role_object = sts_client.assume_role(
            RoleArn=assume_role,
            RoleSessionName=session_name
        )

        lg.info(f'Assumed role {assume_role} with session name {session_name}')
        credentials = assumed_role_object['Credentials']

        assume_params = {
            'aws_access_key_id': credentials['AccessKeyId'],
            'aws_secret_access_key': credentials['SecretAccessKey'],
            'aws_session_token': credentials['SessionToken']
        }

        if region:
            lg.info(f'Using AWS region: {region} for assumed role')
            assume_params['region_name'] = region

        lg.info('Creating AWS session with assumed role')
        session = boto3.Session(**assume_params)  # type: ignore

    if resource:
        result = session.resource(service)
    else:
        result = session.client(service)

    return result


# Client factories
def get_sts_client(obj) -> STSClient:
    return cast(STSClient, get_aws_client('sts', obj))


def get_s3_client(obj) -> S3Client:
    return cast(S3Client, get_aws_client('s3', obj))


def get_dynamodb_client(obj) -> DynamoDBClient:
    return cast(DynamoDBClient, get_aws_client('dynamodb', obj))


def get_route53_client(obj) -> Route53Client:
    return cast(Route53Client, get_aws_client('route53', obj))


# Resource factories
def get_dynamodb_resource(obj) -> DynamoDBServiceResource:
    return cast(DynamoDBServiceResource, get_aws_client('dynamodb', obj, resource=True))
