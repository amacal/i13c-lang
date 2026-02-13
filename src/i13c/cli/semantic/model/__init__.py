from typing import (
    Any,
    Iterable,
    List,
    Protocol,
    Tuple,
    TypeVar,
)

import click

from i13c import lex, par, src
from i13c.cli import unwrap
from i13c.cli.semantic.model.abstract import AbstractListExtractor, ListItem
from i13c.cli.semantic.model.entities import ENTITIES
from i13c.cli.semantic.model.indices import INDICES
from i13c.cli.semantic.model.syntax import SYNTAX
from i13c.core.mapping import Identified
from i13c.core.table import Table, draw_table
from i13c.graph.artifacts import GraphArtifacts
from i13c.graph.nodes import run as run_graph


def draw_list(
    extractor: AbstractListExtractor[ListItem], artifacts: GraphArtifacts
) -> Table:
    entries = extractor.extract(artifacts)
    rows = [extractor.rows(entry) for entry in entries]

    return draw_table(extractor.headers(), rows)


class Showable(Protocol):
    def show(self) -> Iterable[str]: ...


SemanticId = TypeVar("SemanticId", covariant=True)
SemanticNode = TypeVar("SemanticNode", covariant=True)


class OneToOneLike(Protocol[SemanticId, SemanticNode]):
    def items(self) -> Iterable[Tuple[SemanticId, SemanticNode]]: ...


class OneToManyLike(Protocol[SemanticId, SemanticNode]):
    def items(self) -> Iterable[Tuple[SemanticId, Iterable[SemanticNode]]]: ...


def list_one2one_semantic(
    extractor: AbstractListExtractor[Any], artifacts: GraphArtifacts
) -> None:
    for line in draw_list(extractor, artifacts).entries:
        click.echo(line)


def show_one2one_semantic(
    nodes: OneToOneLike[Identified, Showable], node_id: int
) -> None:
    for id, node in nodes.items():
        if id.value == node_id:
            click.echo(f"{id.identify(2)}")
            for line in node.show():
                click.echo(f"  {line}")


def load_artifacts(path: str) -> GraphArtifacts:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    code = src.open_text(text)
    tokens = unwrap(lex.tokenize(code), source=code)
    program = unwrap(par.parse(code, tokens), source=code)
    artifacts = run_graph(program)

    return artifacts


def attach_one2one_commands(
    target: click.Group, node: str, extractor: AbstractListExtractor[Any]
) -> List[click.Command]:

    # introduce a sub-command group for each semantic mapping
    @target.group(node)
    def group() -> None:
        pass

    @group.command("list")
    @click.argument("path", type=click.Path(exists=True))
    def list(path: str) -> None:
        list_one2one_semantic(extractor, load_artifacts(path))

    return [list]


def attach(target: click.Group) -> List[click.Command]:
    commands: List[click.Command] = []

    @target.group("model")
    def model() -> None:
        pass

    for key, extractor in ENTITIES.items():
        commands.extend(attach_one2one_commands(model, key, extractor))

    for key, extractor in INDICES.items():
        commands.extend(attach_one2one_commands(model, key, extractor))

    for key, extractor in SYNTAX.items():
        commands.extend(attach_one2one_commands(model, key, extractor))

    return commands
