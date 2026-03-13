import json
import click

from botobuddy.common import get_sts_client


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
