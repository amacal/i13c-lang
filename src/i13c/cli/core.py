import json
import sys
from collections.abc import Iterable
from functools import partial
from typing import Any, NoReturn

import click

from i13c.core.diagnostics import Diagnostic, show
from i13c.core.result import Result, unwrap
from i13c.syntax.source import SourceCode


class BytesAsTextEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, bytes):
            return o.decode("utf-8", errors="surrogateescape")

        return super().default(o)


def emit_and_exit(
    messages: Iterable[Diagnostic], /, source: SourceCode
) -> NoReturn:
    for message in messages:
        click.echo(
            f"Error {message.code} at offset {message.ref.offset}: {message.message}"
        )

        click.echo("\n")
        click.echo(show(source, message))
        click.echo("\n")

    sys.exit(1)


def unwrap_result[A](
    result: Result[A, list[Diagnostic]], /, source: SourceCode
) -> A:
    return unwrap(result, partial(emit_and_exit, source=source))
