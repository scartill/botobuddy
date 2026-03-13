import click
import json
from pathlib import Path

from botobuddy.common import get_aws_client
from botobuddy.logger import logger


def import_commands(parent):
    """Register Route53 commands with the main CLI group.

    Args:
        parent (click.Group): The parent CLI group to attach to.
    """
    parent.add_command(route53_group)
    # Backward-compatible alias for the previous group name.
    parent.add_command(route53_group, name='route53-group')


@click.group(name='route53')
def route53_group():
    """Route53 operations and management."""
    pass


@route53_group.command(name='export')
@click.pass_obj
@click.argument('hosted_zone_id')
def export_hosted_zone(obj, hosted_zone_id):
    """Export all resource record sets from a specified hosted zone.

    Args:
        obj (dict): Global Click configuration object.
        hosted_zone_id (str): The ID of the Route53 hosted zone to export.
    """
    client = get_aws_client('route53', obj)
    response = client.list_resource_record_sets(HostedZoneId=hosted_zone_id)  # type: ignore
    click.echo(json.dumps(response['ResourceRecordSets'], indent=2))

# Backward-compatible alias for the previous export command name.
route53_group.add_command(export_hosted_zone, name='export-hosted-zone')


@route53_group.command(name='import')
@click.pass_obj
@click.option('--filename', '-f', required=True, type=str)
@click.argument('hosted_zone_id')
def import_hosted_zone(obj, hosted_zone_id, filename):
    """Import resource record sets into a hosted zone, skipping NS and SOA.

    Args:
        obj (dict): Global Click configuration object.
        hosted_zone_id (str): The destination hosted zone ID.
        filename (str): Path to the JSON file containing record sets.
    """
    client = get_aws_client('route53', obj)
    records = json.loads(Path(filename).read_text())

    logger.info(f'Importing {len(records)} records to {hosted_zone_id}')

    for record in records:
        if record['Type'] in ['NS', 'SOA']:
            continue

        client.change_resource_record_sets(  # type: ignore
            HostedZoneId=hosted_zone_id,
            ChangeBatch={'Changes': [
                {'Action': 'UPSERT', 'ResourceRecordSet': record}
            ]}
        )

# Backward-compatible alias for the previous import command name.
route53_group.add_command(import_hosted_zone, name='import-hosted-zone')
