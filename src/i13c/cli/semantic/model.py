from typing import Iterable, List, Protocol, Tuple, TypeVar

import click

from i13c import lex, par, src
from i13c.cli import unwrap
from i13c.sem.infra import Descriptive, Identified
from i13c.sem.model import build_semantic_graph
from i13c.sem.syntax import build_syntax_graph

SemanticId = TypeVar("SemanticId", bound=Identified, covariant=True)
SemanticNode = TypeVar("SemanticNode", bound=Descriptive, covariant=True)


class OneToOneLike(Protocol[SemanticId, SemanticNode]):
    def items(self) -> Iterable[Tuple[SemanticId, SemanticNode]]: ...


class ListOne2OneLike(Protocol):
    def __call__(self, nodes: OneToOneLike[Identified, Descriptive]) -> None: ...


def list_one2one_semantic(nodes: OneToOneLike[Identified, Descriptive]) -> None:
    for id, node in nodes.items():
        click.echo(f"{id.identify(2)} {node.describe()}")


def attach(target: click.Group) -> List[click.Command]:

    @target.group("model")
    @click.argument("node", type=str)
    @click.pass_context
    def model_group(ctx: click.Context, node: str) -> None:
        ctx.obj = {
            "node": node,
            "list": list_one2one_semantic,
        }

    @model_group.command("list")
    @click.argument("path", type=click.Path(exists=True))
    @click.pass_context
    def list_command(ctx: click.Context, path: str) -> None:
        node: str = ctx.obj["node"]
        list: ListOne2OneLike = ctx.obj["list"]
        target: OneToOneLike[Identified, Descriptive]

        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        code = src.open_text(text)
        tokens = unwrap(lex.tokenize(code), source=code)
        program = unwrap(par.parse(code, tokens), source=code)
        graph = build_syntax_graph(program)
        model = build_semantic_graph(graph)

        match node:
            case "literals":
                target = model.basic.literals
            case "instructions":
                target = model.basic.instructions
            case "snippets":
                target = model.basic.snippets
            case "functions":
                target = model.basic.functions
            case "callsites":
                target = model.basic.callsites
            case "entrypoints":
                target = model.live.entrypoints
            case "resolution-by-callsite":
                target = model.indices.resolution_by_callsite
            case "resolution-by-instruction":
                target = model.indices.resolution_by_instruction
            case "terminality-by-function":
                target = model.indices.terminality_by_function
            case "flowgraph-by-function":
                target = model.indices.flowgraph_by_function
            case _:
                raise ValueError(f"unknown semantic node type: {node!r}")

        list(target)

    return [list_command]
