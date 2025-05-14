import boto3
import click
import json
import logging as lg
from pathlib import Path


@click.group()
@click.option('--profile', '-p', default='default')
@click.pass_context
def cli(ctx, profile):
    ctx.ensure_object(dict)
    lg.info(f'Using profile: {profile}')
    boto3.setup_default_session(profile_name=profile)


@cli.command()
@click.argument('hosted_zone_id')
def export_hosted_zone(hosted_zone_id):
    client = boto3.client('route53')
    response = client.list_resource_record_sets(HostedZoneId=hosted_zone_id)
    print(json.dumps(response['ResourceRecordSets'], indent=2))


@cli.command()
@click.option('--filename', '-f', required=True, type=str)
@click.argument('hosted_zone_id')
def import_hosted_zone(hosted_zone_id, filename):
    client = boto3.client('route53')
    records = json.loads(Path(filename).read_text())

    lg.info(
        f'Importing {len(records)} records to {hosted_zone_id}'
        ' (skipping NS and SOA)'
    )

    for record in records:
        if record['Type'] in ['NS', 'SOA']:
            continue

        client.change_resource_record_sets(
            HostedZoneId=hosted_zone_id,
            ChangeBatch={'Changes': [
                {'Action': 'UPSERT', 'ResourceRecordSet': record}
            ]}
        )


cli.add_command(export_hosted_zone)
cli.add_command(import_hosted_zone)


def main():
    lg.basicConfig(level=lg.INFO)
    cli()


if __name__ == '__main__':
    main()
