import json
import os
from dataclasses import asdict

import click

from i13c import elf, lex, par, src
from i13c.cli.core import BytesAsTextEncoder, emit_and_exit, unwrap
from i13c.cli.semantic import attach
from i13c.encoding import encode
from i13c.graph.nodes import run as run_graph


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


@i13c.command("elf")
@click.argument("path", type=click.Path(exists=True))
def elf_command(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    code = src.open_text(text)
    tokens = unwrap(lex.tokenize(code), source=code)

    program = unwrap(par.parse(code, tokens), source=code)
    artifacts = run_graph(program)

    if artifacts.rules().count() > 0:
        emit_and_exit(artifacts.rules().enumerate(), source=code)

    llg = artifacts.llvm_graph()
    assert llg is not None

    flow = llg.instructions()
    binary = encode(list(flow))
    executable = elf.emit(binary)

    with open("a.out", "wb") as f:
        f.write(executable)

    os.chmod("a.out", 0o755)


attach(i13c)
