import json
import os
import sys
from dataclasses import asdict
from functools import partial
from typing import Any, Iterable, List, NoReturn, Protocol, Tuple, TypeVar

import click

from i13c import diag, elf, enc, ld, lex, low, par, res, sem, src
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


class BytesAsTextEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, bytes):
            return o.decode("utf-8", errors="surrogateescape")

        return super().default(o)


def emit_and_exit(
    diagnostics: List[diag.Diagnostic], /, source: src.SourceCode
) -> NoReturn:
    for diagnostic in diagnostics:
        click.echo(
            f"Error {diagnostic.code} at offset {diagnostic.ref.offset}: {diagnostic.message}"
        )

        if diagnostic.ref.length > 0:
            click.echo("\n")
            click.echo(diag.show(source, diagnostic))
            click.echo("\n")

    sys.exit(1)


def unwrap(
    result: res.Result[res.A, List[diag.Diagnostic]], /, source: src.SourceCode
) -> res.A:
    return res.unwrap(result, partial(emit_and_exit, source=source))


@click.group()
def i13c():
    pass


@i13c.command("lex")
@click.argument("path", type=click.Path(exists=True))
def lex_command(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    code = src.open_text(text)
    tokens = unwrap(lex.tokenize(code), source=code)

    for token in tokens:
        key = f"{token.code:03}:{token.offset:04}:{token.length:02}"
        name = f"{lex.TOKEN_NAMES[token.code]:<15}"
        value = code.extract(token)

        click.echo(f"{key}:{name} -> {value!r}")


@i13c.command("ast")
@click.argument("path", type=click.Path(exists=True))
def ast_command(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    code = src.open_text(text)
    tokens = unwrap(lex.tokenize(code), source=code)
    program = unwrap(par.parse(code, tokens), source=code)

    click.echo(json.dumps(asdict(program), cls=BytesAsTextEncoder))


@i13c.command("syntax")
@click.argument("node", type=str)
@click.argument("path", type=click.Path(exists=True))
def syntax_command(node: str, path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    code = src.open_text(text)
    tokens = unwrap(lex.tokenize(code), source=code)
    program = unwrap(par.parse(code, tokens), source=code)

    graph = build_syntax_graph(program)
    data = graph.as_dict(node)

    click.echo(json.dumps(data, cls=BytesAsTextEncoder))


@i13c.group("model")
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


@i13c.command("ir")
@click.argument("path", type=click.Path(exists=True))
def ir_command(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    code = src.open_text(text)
    tokens = unwrap(lex.tokenize(code), source=code)
    program = unwrap(par.parse(code, tokens), source=code)

    graph = build_syntax_graph(program)
    model = build_semantic_graph(graph)

    if diagnostics := sem.validate(model, program):
        emit_and_exit(diagnostics, source=code)

    unit = unwrap(low.lower(model), source=code)

    for idx, codeblock in enumerate(unit.codeblocks):
        click.echo(f"Codeblock: {idx}")

        for instruction in codeblock.instructions:
            click.echo(f"  {str(instruction)}")

        if idx < len(unit.codeblocks) - 1:
            click.echo("")


@i13c.command("bin")
@click.argument("path", type=click.Path(exists=True))
def bin_command(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    code = src.open_text(text)
    tokens = unwrap(lex.tokenize(code), source=code)
    program = unwrap(par.parse(code, tokens), source=code)

    graph = build_syntax_graph(program)
    model = build_semantic_graph(graph)

    if diagnostics := sem.validate(model, program):
        emit_and_exit(diagnostics, source=code)

    unit = unwrap(low.lower(model), source=code)
    linked = unwrap(ld.link(unit), source=code)
    binary = enc.encode(linked)

    sys.stdout.buffer.write(binary)


@i13c.command("elf")
@click.argument("path", type=click.Path(exists=True))
def elf_command(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    code = src.open_text(text)
    tokens = unwrap(lex.tokenize(code), source=code)
    program = unwrap(par.parse(code, tokens), source=code)

    graph = build_syntax_graph(program)
    model = build_semantic_graph(graph)

    if diagnostics := sem.validate(model, program):
        emit_and_exit(diagnostics, source=code)

    unit = unwrap(low.lower(model), source=code)
    linked = unwrap(ld.link(unit), source=code)
    binary = enc.encode(linked)
    executable = elf.emit(binary)

    with open("a.out", "wb") as f:
        f.write(executable)

    os.chmod("a.out", 0o755)
