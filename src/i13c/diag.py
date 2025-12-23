from dataclasses import dataclass

from i13c import src


@dataclass(kw_only=True)
class Diagnostic:
    ref: src.SpanLike
    code: str
    message: str


def show(source: src.SourceCode, diagnostic: Diagnostic) -> str:
    start = source.data.rfind(b"\n", 0, diagnostic.ref.offset)
    end = source.data.find(b"\n", diagnostic.ref.offset + diagnostic.ref.length)

    start = 0 if start == -1 else start + 1
    end = len(source.data) if end == -1 else end

    caret_start = diagnostic.ref.offset - start
    caret_length = diagnostic.ref.length

    line = source.data[start:end]
    caret = b" " * caret_start + b"^" * caret_length
    error = b" " * caret_start + b"|-> " + diagnostic.message.encode("utf-8")

    return (
        line.decode("utf-8")
        + "\n"
        + caret.decode("utf-8")
        + "\n"
        + error.decode("utf-8")
    )
