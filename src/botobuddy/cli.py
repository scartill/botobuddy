import click
import logging as lg
import sys

import botobuddy.s3 as s3
import botobuddy.dynamo as dynamo
import botobuddy.route53 as route53
import botobuddy.auth as auth
import botobuddy.sagemaker as sagemaker


def setup_logging(verbose):
    lg.basicConfig(level=lg.INFO if not verbose else lg.DEBUG)


@click.group()
@click.option('--verbose', is_flag=True, help='Enable debug logging')
@click.option('--profile', help='AWS profile name to use')
@click.option('--region', help='AWS region to use')
@click.option('--assume-role', help='AWS role ARN to assume')
@click.pass_context
def cli(ctx, verbose, **kwargs):
    '''Extended AWS Operations CLI'''
    setup_logging(verbose)
    ctx.ensure_object(dict)
    ctx.obj.update(kwargs)


def main():
    try:
        s3.import_commands(cli)
        dynamo.import_commands(cli)
        route53.import_commands(cli)
        auth.import_commands(cli)
        sagemaker.import_commands(cli)
        cli()
        sys.exit(0)

    except Exception as e:
        lg.error(e)
        sys.exit(1)


if __name__ == '__main__':
    main()
