from dataclasses import dataclass
from typing import Callable, Dict, Iterable, List, Optional, Protocol, Tuple, TypeVar

import click

from i13c import lex, par, src
from i13c.cli import unwrap
from i13c.core.mapping import Descriptive, Identified
from i13c.sem.model import SemanticGraph, build_semantic_graph
from i13c.sem.syntax import build_syntax_graph


class Showable(Protocol):
    def show(self) -> Iterable[str]: ...


SemanticId = TypeVar("SemanticId", covariant=True)
SemanticNode = TypeVar("SemanticNode", covariant=True)


class OneToOneLike(Protocol[SemanticId, SemanticNode]):
    def items(self) -> Iterable[Tuple[SemanticId, SemanticNode]]: ...


class OneToManyLike(Protocol[SemanticId, SemanticNode]):
    def items(self) -> Iterable[Tuple[SemanticId, Iterable[SemanticNode]]]: ...


ExtractOneToOne = Callable[[SemanticGraph], OneToOneLike[Identified, Descriptive]]
ExtractOneToMany = Callable[[SemanticGraph], OneToManyLike[Identified, Descriptive]]


@dataclass(kw_only=True)
class OneToOneFeature:
    list: Optional[Callable[[SemanticGraph], OneToOneLike[Identified, Descriptive]]] = (
        None
    )
    show: Optional[Callable[[SemanticGraph], OneToOneLike[Identified, Showable]]] = None


ONE2ONE: Dict[str, OneToOneFeature] = {
    "literals": OneToOneFeature(list=lambda model: model.basic.literals),
    "instructions": OneToOneFeature(list=lambda model: model.basic.instructions),
    "snippets": OneToOneFeature(list=lambda model: model.basic.snippets),
    "functions": OneToOneFeature(list=lambda model: model.basic.functions),
    "callsites": OneToOneFeature(list=lambda model: model.basic.callsites),
    "terminality-by-function": OneToOneFeature(
        list=lambda model: model.indices.terminality_by_function
    ),
    "resolution-by-instruction": OneToOneFeature(
        list=lambda model: model.indices.resolution_by_instruction
    ),
    "resolution-by-callsite": OneToOneFeature(
        list=lambda model: model.indices.resolution_by_callsite
    ),
    "flowgraph-by-function": OneToOneFeature(
        list=lambda model: model.indices.flowgraph_by_function,
        show=lambda model: model.indices.flowgraph_by_function,
    ),
}

ONE2MANY: Dict[str, ExtractOneToMany] = {
    "calls-by-caller": lambda model: model.callgraph.calls_by_caller,
    "calls-by-callee": lambda model: model.callgraph.calls_by_callee,
}


class ListOne2OneLike(Protocol):
    def __call__(self, nodes: OneToOneLike[Identified, Descriptive]) -> None: ...


def list_one2one_semantic(nodes: OneToOneLike[Identified, Descriptive]) -> None:
    for id, node in nodes.items():
        click.echo(f"{id.identify(2)} {node.describe()}")


def list_one2many_semantic(nodes: OneToManyLike[Identified, Descriptive]) -> None:
    for id, node_list in nodes.items():
        for node in node_list:
            click.echo(f"{id.identify(2)} {node.describe()}")


def show_one2one_semantic(
    nodes: OneToOneLike[Identified, Showable], node_id: int
) -> None:
    for id, node in nodes.items():
        if id.value == node_id:
            click.echo(f"{id.identify(2)}")
            for line in node.show():
                click.echo(f"  {line}")


def load_model(path: str) -> SemanticGraph:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    code = src.open_text(text)
    tokens = unwrap(lex.tokenize(code), source=code)
    program = unwrap(par.parse(code, tokens), source=code)
    graph = build_syntax_graph(program)
    model = build_semantic_graph(graph)

    return model


def attach_one2one_commands(
    target: click.Group, node: str, extract: OneToOneFeature
) -> List[click.Command]:
    commands: List[click.Command] = []

    # introduce a sub-command group for each semantic mapping
    @target.group(node)
    def group() -> None:
        pass

    # introduce a "list" command for each mapping
    if extract.list is not None:

        @group.command("list")
        @click.argument("path", type=click.Path(exists=True))
        def list(path: str) -> None:
            if extract.list is not None:
                list_one2one_semantic(extract.list(load_model(path)))

            commands.append(list)

    # introduce a "show" command for each mapping
    if extract.show is not None:

        @group.command("show")
        @click.option("--node-id", type=int, required=True)
        @click.argument("path", type=click.Path(exists=True))
        def show(node_id: int, path: str) -> None:
            if extract.show is not None:
                show_one2one_semantic(extract.show(load_model(path)), node_id)

        commands.append(show)

    return commands


def attach_one2many_commands(
    target: click.Group, node: str, extract: ExtractOneToMany
) -> List[click.Command]:

    # introduce a sub-command group for each semantic mapping
    @target.group(node)
    def group() -> None:
        pass

    # introduce a "list" command for each mapping
    @group.command("list")
    @click.argument("path", type=click.Path(exists=True))
    def list(path: str) -> None:
        list_one2many_semantic(extract(load_model(path)))

    return [list]


def attach(target: click.Group) -> List[click.Command]:
    commands: List[click.Command] = []

    @target.group("model")
    def model() -> None:
        pass

    for key, extract in ONE2ONE.items():
        commands.extend(attach_one2one_commands(model, key, extract))

    for key, extract in ONE2MANY.items():
        commands.extend(attach_one2many_commands(model, key, extract))

    return commands
