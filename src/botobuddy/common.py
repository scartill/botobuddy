from typing import cast

import randomname
import boto3
from botocore.config import Config
from types_boto3_s3 import S3Client
from types_boto3_dynamodb import DynamoDBClient, DynamoDBServiceResource
from types_boto3_route53 import Route53Client
from types_boto3_sts import STSClient
from types_boto3_sagemaker import SageMakerClient
from types_boto3_cognito_idp import CognitoIdentityProviderClient
from types_boto3_cloudformation import CloudFormationClient
from types_boto3_apigateway import APIGatewayClient
from types_boto3_secretsmanager import SecretsManagerClient
from types_boto3_ssm import SSMClient
from types_boto3_lambda import LambdaClient

from botobuddy.logger import logger


type AWSClient = (
    S3Client
    | DynamoDBClient
    | DynamoDBServiceResource
    | Route53Client
    | STSClient
    | SageMakerClient
    | CognitoIdentityProviderClient
    | CloudFormationClient
    | APIGatewayClient
    | SecretsManagerClient
    | SSMClient
    | LambdaClient
)


def get_aws_session(session_config: dict = {}) -> boto3.Session:
    """Create and return an AWS session with optional profile and region

    Args:
        session_config: A dictionary of session configuration options:
        - profile: The AWS profile to use
        - region: The AWS region to use
        - assume_role: The AWS role ARN to assume
        - session_name: The name of the session

    Returns:
        A boto3.Session object
    """

    profile = session_config.get('profile')
    region = session_config.get('region')

    params = {}

    if profile:
        logger.info(f'Using AWS profile: {profile}')
        params['profile_name'] = profile

    if region:
        logger.info(f'Using AWS region: {region}')
        params['region_name'] = region

    logger.info('Creating AWS session')
    session = boto3.Session(**params)

    if assume_role := session_config.get('assume_role'):
        session_name = randomname.get_name()
        sts_client = session.client('sts')

        assumed_role_object = sts_client.assume_role(RoleArn=assume_role, RoleSessionName=session_name)

        logger.info(f'Assumed role {assume_role} with session name {session_name}')

        # Log only the assumed role user details to avoid exposing sensitive credentials in debug logs
        assumed_role_user = assumed_role_object.get('AssumedRoleUser', {})
        logger.debug(f'Assumed role user: {assumed_role_user}')

        credentials = assumed_role_object['Credentials']

        assume_params = {
            'aws_access_key_id': credentials['AccessKeyId'],
            'aws_secret_access_key': credentials['SecretAccessKey'],
            'aws_session_token': credentials['SessionToken'],
        }

        if region:
            logger.info(f'Using AWS region: {region} for assumed role')
            assume_params['region_name'] = region

        logger.info('Creating AWS session with assumed role')
        session = boto3.Session(**assume_params)  # type: ignore

    return session


def get_aws_client(service, session_config={}, resource=False, core_config: dict | None = None) -> AWSClient:
    """Create and return an AWS client or resource.

    Args:
        service: The AWS service name (e.g., 's3', 'dynamodb').
        session_config: Configuration for the AWS session.
        resource: Whether to return a Boto3 resource instead of a client.
        core_config: Optional botocore configuration dictionary.

    Returns:
        An AWS client or resource object.
    """
    session = get_aws_session(session_config)

    client_params = {'service_name': service}

    if core_config:
        logger.debug(f'Using core session config: {core_config}')
        botocore_config = Config(**core_config)
        client_params['config'] = botocore_config

    if resource:
        result = session.resource(**client_params)
    else:
        result = session.client(**client_params)

    return result


# Client factories
def get_sts_client(session_config={}) -> STSClient:
    """Get an STS client.

    Args:
        session_config (dict): Optional AWS session configuration.

    Returns:
        STSClient: A Boto3 STS client.
    """
    return cast(STSClient, get_aws_client('sts', session_config))


def get_s3_client(session_config={}, core_config: dict | None = None) -> S3Client:
    """Get an S3 client.

    Args:
        session_config (dict): Optional AWS session configuration.
        core_config (dict): Optional botocore configuration.

    Returns:
        S3Client: A Boto3 S3 client.
    """
    return cast(S3Client, get_aws_client('s3', session_config, core_config=core_config))


def get_dynamodb_client(session_config: dict | None = None) -> DynamoDBClient:
    """Get a DynamoDB client.

    Args:
        session_config (dict): Optional AWS session configuration.

    Returns:
        DynamoDBClient: A Boto3 DynamoDB client.
    """
    if session_config is None:
        session_config = {}
    return cast(DynamoDBClient, get_aws_client('dynamodb', session_config))


def get_route53_client(session_config: dict | None = None) -> Route53Client:
    """Get a Route53 client.

    Args:
        session_config (dict): Optional AWS session configuration.

    Returns:
        Route53Client: A Boto3 Route53 client.
    """
    if session_config is None:
        session_config = {}
    return cast(Route53Client, get_aws_client('route53', session_config))


def get_sagemaker_client(session_config: dict | None = None) -> SageMakerClient:
    """Get a SageMaker client.

    Args:
        session_config (dict): Optional AWS session configuration.

    Returns:
        SageMakerClient: A Boto3 SageMaker client.
    """
    if session_config is None:
        session_config = {}
    return cast(SageMakerClient, get_aws_client('sagemaker', session_config))


def get_cognito_client(session_config: dict | None = None) -> CognitoIdentityProviderClient:
    """Get a Cognito Identity Provider client.

    Args:
        session_config (dict): Optional AWS session configuration.

    Returns:
        CognitoIdentityProviderClient: A Boto3 Cognito client.
    """
    if session_config is None:
        session_config = {}
    return cast(CognitoIdentityProviderClient, get_aws_client('cognito-idp', session_config))


def get_cloudformation_client(session_config: dict | None = None) -> CloudFormationClient:
    """Get a CloudFormation client.

    Args:
        session_config (dict): Optional AWS session configuration.

    Returns:
        CloudFormationClient: A Boto3 CloudFormation client.
    """
    if session_config is None:
        session_config = {}
    return cast(CloudFormationClient, get_aws_client('cloudformation', session_config))


def get_apigateway_client(session_config: dict | None = None) -> APIGatewayClient:
    """Get an API Gateway client.

    Args:
        session_config (dict): Optional AWS session configuration.

    Returns:
        APIGatewayClient: A Boto3 API Gateway client.
    """
    if session_config is None:
        session_config = {}
    return cast(APIGatewayClient, get_aws_client('apigateway', session_config))


def get_secretsmanager_client(session_config: dict | None = None) -> SecretsManagerClient:
    """Get a Secrets Manager client.

    Args:
        session_config (dict): Optional AWS session configuration.

    Returns:
        SecretsManagerClient: A Boto3 Secrets Manager client.
    """
    if session_config is None:
        session_config = {}
    return cast(SecretsManagerClient, get_aws_client('secretsmanager', session_config))


def get_ssm_client(session_config: dict | None = None) -> SSMClient:
    """Get an SSM client.

    Args:
        session_config (dict): Optional AWS session configuration.

    Returns:
        SSMClient: A Boto3 SSM client.
    """
    if session_config is None:
        session_config = {}
    return cast(SSMClient, get_aws_client('ssm', session_config))


def get_lambda_client(session_config: dict | None = None) -> LambdaClient:
    """Get a Lambda client.

    Args:
        session_config (dict): Optional AWS session configuration.

    Returns:
        LambdaClient: A Boto3 Lambda client.
    """
    if session_config is None:
        session_config = {}
    return cast(LambdaClient, get_aws_client('lambda', session_config))


# Resource factories
def get_dynamodb_resource(session_config: dict | None = None) -> DynamoDBServiceResource:
    """Get a DynamoDB resource.

    Args:
        session_config (dict): Optional AWS session configuration.

    Returns:
        DynamoDBServiceResource: A Boto3 DynamoDB resource.
    """
    if session_config is None:
        session_config = {}
    return cast(
        DynamoDBServiceResource,
        get_aws_client('dynamodb', session_config, resource=True),
    )
