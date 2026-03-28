from dataclasses import dataclass

from i13c.syntax.source import SourceCode, SpanLike


@dataclass(kw_only=True)
class Diagnostic:
    ref: SpanLike
    code: str
    message: str


def show(source: SourceCode, diagnostic: Diagnostic) -> str:

    # sanity check to ensure diagnostics always have a message
    assert diagnostic.message, "Diagnostic message cannot be empty"

    start = source.data.rfind(b"\n", 0, diagnostic.ref.offset)
    end = source.data.find(b"\n", diagnostic.ref.offset)

    start = 0 if start == -1 else start + 1
    end = len(source.data) if end == -1 else end
    line = source.data[start:end]

    # respect zero-length spans by showing a single caret
    # and avoid drawing carets beyond the current line for multi-line spans
    caret_start = min(max(0, diagnostic.ref.offset - start), len(line))
    remaining = max(0, len(line) - caret_start)
    caret_length = min(max(1, diagnostic.ref.length), max(1, remaining))

    caret = b" " * caret_start + b"^" * caret_length
    error = (
        b" " * caret_start
        + b"|-> "
        + diagnostic.message.encode("utf-8").splitlines()[0]
    )

    return (
        line.decode("utf-8")
        + "\n"
        + caret.decode("utf-8")
        + "\n"
        + error.decode("utf-8")
    )
