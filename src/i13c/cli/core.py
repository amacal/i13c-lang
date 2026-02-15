import json
import sys
from functools import partial
from typing import Any, Iterable, List, NoReturn

import click

from i13c import diag, res, src


class BytesAsTextEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, bytes):
            return o.decode("utf-8", errors="surrogateescape")

        return super().default(o)


def emit_and_exit(
    diagnostics: Iterable[diag.Diagnostic], /, source: src.SourceCode
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
