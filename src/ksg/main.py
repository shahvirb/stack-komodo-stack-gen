from jinja2 import Environment, FileSystemLoader, Template
from pathlib import Path
import click
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
    """
    Generate all the stack configurations from a parent directory.

    DIRECTORY: parent directory containing all the stack-* dirs
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
    """
    Generate a single stack configuration from a directory.

    DIRECTORY: directory containing the single stack files
    """
    dir_path = Path(directory).resolve()
    stack_name = dir_path.name
    server_name = os.environ.get("HOSTNAME") or os.environ.get(
        "COMPUTERNAME", "localhost"
    )

    # If any files with .tpl extension exist, set op_unpack to True
    op_unpack = bool(list(dir_path.rglob("*.tpl")))

    template = get_template("single.toml")
    rendered = template.render(
        stack_name=stack_name, server_name=server_name, op_unpack=op_unpack
    )

    click.echo(rendered)


if __name__ == "__main__":
    cli()
