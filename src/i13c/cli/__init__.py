import json
import os
import sys
from dataclasses import asdict

import click

from i13c import elf, enc, lex, par, sem, src
from i13c.cli.core import BytesAsTextEncoder, emit_and_exit, unwrap
from i13c.cli.semantic import attach
from i13c.lowering.build import build_low_level_graph
from i13c.sem.model import build_semantic_graph
from i13c.sem.syntax import build_syntax_graph


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


@i13c.command("llg")
@click.argument("path", type=click.Path(exists=True))
def llg_command(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    code = src.open_text(text)
    tokens = unwrap(lex.tokenize(code), source=code)
    program = unwrap(par.parse(code, tokens), source=code)

    graph = build_syntax_graph(program)
    model = build_semantic_graph(graph)

    if diagnostics := sem.validate(model, program):
        emit_and_exit(diagnostics, source=code)

    llg = build_low_level_graph(model)

    for idx, (bid, block) in enumerate(llg.nodes.items()):
        click.echo(f"Block: {bid.value}")
        click.echo(f"  Origin: {block.origin.identify(2)}")
        click.echo(f"  Edges: {[succ.value for succ in llg.forward.find(bid)]}")
        click.echo(f"  Terminator: {block.terminator}")

        click.echo("  Instructions:")
        for instruction in block.instructions:
            click.echo(f"    {str(instruction)}")

        if idx < llg.nodes.size() - 1:
            click.echo("")


@i13c.command("linear")
@click.argument("path", type=click.Path(exists=True))
def linear_command(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    code = src.open_text(text)
    tokens = unwrap(lex.tokenize(code), source=code)
    program = unwrap(par.parse(code, tokens), source=code)

    graph = build_syntax_graph(program)
    model = build_semantic_graph(graph)

    if diagnostics := sem.validate(model, program):
        emit_and_exit(diagnostics, source=code)

    llg = build_low_level_graph(model)
    flow = llg.instructions()

    for idx, instruction in enumerate(flow):
        click.echo(f"{idx:04}: {str(instruction)}")


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

    llg = build_low_level_graph(model)
    flow = llg.instructions()

    binary = enc.encode(list(flow))
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

    llg = build_low_level_graph(model)
    flow = llg.instructions()

    binary = enc.encode(list(flow))
    executable = elf.emit(binary)

    with open("a.out", "wb") as f:
        f.write(executable)

    os.chmod("a.out", 0o755)


attach(i13c)
