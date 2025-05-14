
import click
import logging as lg
from common import get_aws_client


def import_commands(parent):
    parent.add_command(s3_group)


@click.group(name='s3')
def s3_group():
    pass


@s3_group.command(name='delete-bucket')
@click.argument('bucket_name')
@click.option('--region', help='AWS region of the bucket')
@click.pass_context
def delete_bucket_cmd(ctx, bucket_name, region):
    '''Clean and delete an S3 bucket completely'''
    try:
        profile = ctx.obj.get('profile')
        lg.debug(f'Using AWS profile: {profile}')
        
        # First empty the bucket
        delete_bucket_contents(bucket_name, region, profile)
        
        # Then delete the bucket itself
        delete_bucket(bucket_name, region, profile)

    except Exception as e:
        raise UserWarning('Error deleting bucket') from e


def delete_bucket_contents(bucket_name, region=None, profile=None):
    '''
    Deletes all objects and object versions from the specified S3 bucket
    '''
    lg.info(f'Deleting all objects in bucket: {bucket_name}')
    
    # Create S3 client with optional region and profile
    s3 = get_aws_client('s3', region, profile)
    
    # Delete all objects and their versions
    paginator = s3.get_paginator('list_object_versions')
    page_iterator = paginator.paginate(Bucket=bucket_name)
    
    for page in page_iterator:
        # Delete object versions if they exist
        if 'Versions' in page:
            for version in page['Versions']:
                s3.delete_object(
                    Bucket=bucket_name,
                    Key=version['Key'],
                    VersionId=version['VersionId']
                )
                lg.info(f'Deleted object: {version["Key"]} (version {version["VersionId"]})')
        
        # Delete delete markers if they exist
        if 'DeleteMarkers' in page:
            for marker in page['DeleteMarkers']:
                s3.delete_object(
                    Bucket=bucket_name,
                    Key=marker['Key'],
                    VersionId=marker['VersionId']
                )
                lg.info(f'Deleted delete marker: {marker["Key"]} (version {marker["VersionId"]})')
    
    # Delete objects in a non-versioned bucket
    paginator = s3.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=bucket_name)
    
    objects_to_delete = []
    for page in page_iterator:
        if 'Contents' in page:
            for obj in page['Contents']:
                objects_to_delete.append({'Key': obj['Key']})
                
            if objects_to_delete:
                # Delete in batches of 1000 (AWS limit)
                for i in range(0, len(objects_to_delete), 1000):
                    batch = objects_to_delete[i:i+1000]
                    s3.delete_objects(
                        Bucket=bucket_name,
                        Delete={'Objects': batch}
                    )
                    lg.info(f'Deleted {len(batch)} objects')
                objects_to_delete = []


def delete_bucket(bucket_name, region=None, profile=None):
    '''
    Deletes the specified S3 bucket after emptying it
    '''
    # Create S3 client
    s3 = get_aws_client('s3', region, profile)
    
    try:
        # Delete the bucket
        s3.delete_bucket(Bucket=bucket_name)
        lg.info(f'Bucket {bucket_name} has been deleted successfully')
    except Exception as e:
        lg.error(f'Error deleting bucket: {e}')