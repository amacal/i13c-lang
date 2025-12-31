import click

from i13c.cli.semantic.model import attach as attach_model
from i13c.cli.semantic.syntax import attach as attach_syntax


def attach(target: click.Group) -> None:
    attach_syntax(target)
    attach_model(target)
