from pathlib import Path
import click
from jinja2 import Environment, FileSystemLoader, Template
import os


def get_template(filename: str) -> Template:
    template_dir = Path(__file__).parent.parent.parent / "templates"
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(filename)
    return template


@click.group()
def cli():
    """Komodo Stack Generator CLI"""
    pass


@cli.command()
@click.argument(
    "directory",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
)
def stacks(directory):
    """Render the stacks.toml template

    DIRECTORY: Target directory to use in the template (e.g., '.' for current directory)
    """
    # Resolve directory to absolute path
    absolute_dir = directory.resolve()

    # Get all level 1 child directories that start with "stack-"
    for child_dir in absolute_dir.iterdir():
        if child_dir.is_dir() and child_dir.name.startswith("stack-"):
            single.callback(child_dir)


@cli.command()
@click.argument(
    "directory", type=click.Path(exists=True, file_okay=False, dir_okay=True)
)
def single(directory):
    """Generate a single stack configuration from a directory."""
    dir_path = Path(directory).resolve()
    stack_name = dir_path.name
    server_name = os.environ.get("HOSTNAME") or os.environ.get(
        "COMPUTERNAME", "localhost"
    )
    op_unpack = False

    template = get_template("single.toml")
    rendered = template.render(
        stack_name=stack_name, server_name=server_name, op_unpack=op_unpack
    )

    click.echo(rendered)


if __name__ == "__main__":
    cli()
