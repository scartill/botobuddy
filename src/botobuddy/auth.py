import json
import click

from typing import cast
from types_boto3_sts import STSClient

from botobuddy.common import get_aws_client


def get_sts_client(session_config: dict | None = None, profile: str | None = None) -> STSClient:
    """Get an STS client.

    Args:
        session_config (dict): Optional AWS session configuration.
        profile: Explicit AWS profile name. Takes precedence over session_config['profile'].

    Returns:
        STSClient: A Boto3 STS client.
    """
    if session_config is None:
        session_config = {}

    return cast(STSClient, get_aws_client('sts', session_config, profile=profile))


def import_commands(parent):
    """Import auth commands to the parent Click group.

    Args:
        parent: The parent Click group to add commands to.
    """
    parent.add_command(auth_group)


@click.group(name='auth')
def auth_group():
    """Authentication related commands."""
    pass


@auth_group.command()
@click.pass_obj
def caller(obj):
    """Get the current AWS caller identity.

    Args:
        obj: The context object containing session configuration.
    """
    sts_client = get_sts_client(obj)
    caller_identity = sts_client.get_caller_identity()
    click.echo(json.dumps(caller_identity, indent=4))
