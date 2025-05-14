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
@click.pass_obj
def delete_bucket_cmd(obj, bucket_name):
    '''Clean and delete an S3 bucket completely'''
    try:
        client = get_aws_client('s3', obj)

        # First empty the bucket
        delete_bucket_contents(client, bucket_name)

        # Then delete the bucket itself
        delete_bucket(client, bucket_name)

    except Exception as e:
        raise UserWarning('Error deleting bucket') from e


def delete_bucket_contents(client, bucket_name):
    '''
    Deletes all objects and object versions from the specified S3 bucket
    '''
    lg.info(f'Deleting all objects in bucket: {bucket_name}')

    # Delete all objects and their versions
    paginator = client.get_paginator('list_object_versions')
    page_iterator = paginator.paginate(Bucket=bucket_name)

    for page in page_iterator:
        # Delete object versions if they exist
        if 'Versions' in page:
            for version in page['Versions']:
                client.delete_object(
                    Bucket=bucket_name,
                    Key=version['Key'],
                    VersionId=version['VersionId']
                )
                lg.info(f'Deleted object: {version["Key"]} (version {version["VersionId"]})')

        # Delete delete markers if they exist
        if 'DeleteMarkers' in page:
            for marker in page['DeleteMarkers']:
                client.delete_object(
                    Bucket=bucket_name,
                    Key=marker['Key'],
                    VersionId=marker['VersionId']
                )
                lg.info(f'Deleted delete marker: {marker["Key"]} (version {marker["VersionId"]})')

    # Delete objects in a non-versioned bucket
    paginator = client.get_paginator('list_objects_v2')
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

                    client.delete_objects(
                        Bucket=bucket_name,
                        Delete={'Objects': batch}
                    )

                    lg.info(f'Deleted {len(batch)} objects')

                objects_to_delete = []


def delete_bucket(client, bucket_name):
    '''
    Deletes the specified S3 bucket after emptying it
    '''

    try:
        # Delete the bucket
        client.delete_bucket(Bucket=bucket_name)
        lg.info(f'Bucket {bucket_name} has been deleted successfully')

    except Exception as e:
        raise UserWarning('Error deleting bucket') from e
