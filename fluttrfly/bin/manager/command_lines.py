import click

from ..commands.global_variables import fluttrfly_version
from .commands_manager import CommandsManager


# Here our CLI starts.
@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.version_option(version=fluttrfly_version, help="Print the version information.")
@click.pass_context
def cli(ctx):
    """CLI to streamline the development process for Flutter projects."""
    ctx.obj = CommandsManager()


@cli.command()
@click.option('-v', '--version', is_flag=True, help="Show Fluttrfly environment version.")
@click.option(
    '-r', '--reset', is_flag=True, help="Reset env's version to match Fluttrfly's version."
)
@click.option('-u', '--update', is_flag=True, help="Update the environment.")
@click.option('-f', '--force', is_flag=True, help="Create environment forcibly.")
@click.pass_context
def env(ctx, version, reset, update, force):
    """Create and manage the Fluttrfly environment."""
    cli = ctx.obj
    cli.handle_env(version, reset, update, force)


@cli.command()
@click.option('-m', '--module', type=str, help="Build a structured module", metavar="Module")
@click.option('-a', '--assets', is_flag=True, help="Build structured assets", default=False)
@click.option('-c', '--core', is_flag=True, help="Build core structure", default=False)
@click.pass_context
def build(ctx, module, assets, core):
    """Build various project structures like modules, assets, and core."""
    cli = ctx.obj
    cli.handle_build(module, assets, core)


@cli.command()
@click.option(
    '-r',
    '--riverpod',
    is_flag=True,
    help="Set up the project using Riverpod state management",
    default=False,
)
@click.option(
    '-b',
    '--bloc',
    is_flag=True,
    help="Set up the project using Bloc state management.",
    default=False,
)
@click.pass_context
def setup(ctx, riverpod, bloc):
    """Set up a new Flutter project with the desired state management solution."""
    cli = ctx.obj
    cli.handle_setup(riverpod, bloc)
