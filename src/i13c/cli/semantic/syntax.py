import json
from typing import List

import click

from i13c import lex, par, src
from i13c.cli import BytesAsTextEncoder, unwrap
from i13c.sem.syntax import build_syntax_graph


def attach(target: click.Group) -> List[click.Command]:
    @target.command("syntax")
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

    return [syntax_command]
