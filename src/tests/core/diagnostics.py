from i13c.core.diagnostics import Diagnostic, show
from i13c.syntax.source import Span, open_text


def left(text: str) -> str:
    # keep only non-empty lines
    lines = [line for line in text.strip(' ').splitlines() if line.strip()]

    # count leading spaces for non-empty lines
    margin = min(len(line) - len(line.lstrip()) for line in lines)
    print(margin, lines)

    # remove leading spaces
    return "\n".join(line[margin:] for line in lines)


def can_show_caret_for_non_empty_span():
    source = open_text("mov rax, 0x10")
    diagnostic = Diagnostic(
        ref=Span(offset=9, length=4),
        code="EXXXX",
        message="invalid immediate",
    )

    assert show(source, diagnostic) == left(
        """
            mov rax, 0x10
                     ^^^^
                     |-> invalid immediate
        """
    )


def can_show_caret_for_zero_length_span():
    source = open_text("mov rax, 0x10")
    diagnostic = Diagnostic(
        ref=Span(offset=len(source.data), length=0),
        code="EXXXX",
        message="unexpected end of tokens",
    )

    assert show(source, diagnostic) == left(
        """
            mov rax, 0x10
                         ^
                         |-> unexpected end of tokens
        """
    )
