import click

from botobuddy.common import get_dynamodb_resource, DynamoDBServiceResource
from botobuddy.logger import logger


def import_commands(parent):
    """Import dynamo commands to the parent Click group.

    Args:
        parent: The parent Click group to add commands to.
    """
    parent.add_command(dynamo_group)


@click.group(name='dynamo')
def dynamo_group():
    """DynamoDB related commands."""
    pass


@dynamo_group.command(name='truncate-table')
@click.pass_obj
@click.argument('table_name')
def truncate_table_cmd(obj, table_name):
    """Truncate a DynamoDB table.

    Args:
        obj: The context object containing session configuration.
        table_name: The name of the table to truncate.
    """
    client = get_dynamodb_resource(obj)
    counter = truncate_table(client, table_name)
    logger.info(f'Deleted {counter} items')


def truncate_table(client: DynamoDBServiceResource, table_name: str):
    """Implementation to truncate a DynamoDB table.

    Scans the table for all keys and deletes items in batches.

    Args:
        client: The Boto3 DynamoDB resource.
        table_name: The name of the table to truncate.

    Returns:
        The number of items deleted.
    """
    table = client.Table(table_name)

    # Get the table keys
    tableKeyNames = [key.get('AttributeName') for key in table.key_schema]

    # Only retrieve the keys for each item in the table (minimize data transfer)
    projectionExpression = ', '.join('#' + key for key in tableKeyNames)
    expressionAttrNames = {'#' + key: key for key in tableKeyNames}

    counter = 0

    page = table.scan(
        ProjectionExpression=projectionExpression,
        ExpressionAttributeNames=expressionAttrNames
    )

    with table.batch_writer() as batch:
        while page['Count'] > 0:
            counter += page['Count']

            # Delete items in batches
            for itemKeys in page['Items']:
                batch.delete_item(Key=itemKeys)

            # Fetch the next page
            if 'LastEvaluatedKey' in page:
                page = table.scan(
                    ProjectionExpression=projectionExpression,
                    ExpressionAttributeNames=expressionAttrNames,
                    ExclusiveStartKey=page['LastEvaluatedKey']
                )

            else:
                break

    return counter
