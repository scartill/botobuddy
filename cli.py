import click
import logging as lg
import sys

import s3


def setup_logging(verbose):
    lg.basicConfig(level=lg.INFO if not verbose else lg.DEBUG)


@click.group()
@click.option('--verbose', is_flag=True, help='Enable debug logging')
@click.option('--profile', help='AWS profile name to use')
@click.pass_context
def cli(ctx, verbose, profile):
    '''Extended AWS Operations CLI'''
    setup_logging(verbose)

    # Create a context object to pass to subcommands
    ctx.ensure_object(dict)
    ctx.obj['profile'] = profile


if __name__ == '__main__':
    try:
        s3.import_commands(cli)
        cli()
        sys.exit(0)

    except UserWarning as e:
        lg.error(e)
        sys.exit(1)
