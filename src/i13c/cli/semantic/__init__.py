import click

from i13c.cli.semantic.model import attach as attach_model


def attach(target: click.Group) -> None:
    attach_model(target)
