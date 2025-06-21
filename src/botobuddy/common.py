import logging as lg
from typing import cast

import randomname
import boto3
from botocore.session import Session as BotocoreSession
from types_boto3_s3 import S3Client
from types_boto3_dynamodb import DynamoDBClient, DynamoDBServiceResource
from types_boto3_route53 import Route53Client
from types_boto3_sts import STSClient
from types_boto3_sagemaker import SageMakerClient
from types_boto3_cognito_idp import Client as CognitoClient


type AWSClient = (
    S3Client |
    DynamoDBClient |
    DynamoDBServiceResource |
    Route53Client |
    STSClient |
    SageMakerClient |
    CognitoClient
)


def get_aws_client(
    service,
    cliparams,
    resource=False,
    core_config: dict | None = None
) -> AWSClient:
    '''Create and return an AWS client with optional profile and region'''
    profile = cliparams.get('profile')
    region = cliparams.get('region')

    params = {}

    if profile:
        lg.info(f'Using AWS profile: {profile}')
        params['profile_name'] = profile

    if region:
        lg.info(f'Using AWS region: {region}')
        params['region_name'] = region

    if core_config:
        lg.info(f'Using core session config: {core_config}')
        botocore_session = BotocoreSession()

        for key, value in core_config.items():
            lg.info(f'Setting core session config variable {key} to {value}')
            botocore_session.set_config_variable(key, value)

        params['botocore_session'] = botocore_session

    lg.info('Creating AWS session')
    session = boto3.Session(**params)

    if assume_role := cliparams.get('assume_role'):
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
def get_sts_client(cliparams) -> STSClient:
    return cast(STSClient, get_aws_client('sts', cliparams))


def get_s3_client(cliparams, core_config: dict | None = None) -> S3Client:
    return cast(S3Client, get_aws_client('s3', cliparams, core_config=core_config))


def get_dynamodb_client(cliparams) -> DynamoDBClient:
    return cast(DynamoDBClient, get_aws_client('dynamodb', cliparams))


def get_route53_client(cliparams) -> Route53Client:
    return cast(Route53Client, get_aws_client('route53', cliparams))


def get_sagemaker_client(cliparams) -> SageMakerClient:
    return cast(SageMakerClient, get_aws_client('sagemaker', cliparams))


def get_cognito_client(cliparams) -> CognitoClient:
    return cast(CognitoClient, get_aws_client('cognito-idp', cliparams))


# Resource factories
def get_dynamodb_resource(cliparams) -> DynamoDBServiceResource:
    return cast(DynamoDBServiceResource, get_aws_client('dynamodb', cliparams, resource=True))
