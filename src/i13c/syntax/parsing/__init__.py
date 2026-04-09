from typing import List, Set, Union

from i13c.core import result
from i13c.core.diagnostics import Diagnostic
from i13c.syntax import tree
from i13c.syntax.lexing import TOKEN_NAMES
from i13c.syntax.lexing import Token as LexingToken
from i13c.syntax.lexing import Tokens
from i13c.syntax.parsing.core import (
    FlagAlreadySpecified,
    InvalidHexLiteral,
    ParsingState,
    UnexpectedEndOfTokens,
    UnexpectedKeyword,
    UnexpectedTokenCode,
)
from i13c.syntax.parsing.function import parse_function
from i13c.syntax.parsing.snippet import parse_snippet
from i13c.syntax.source import SourceCode, Span, SpanLike


def parse(
    code: SourceCode, tokens: List[LexingToken]
) -> result.Result[tree.Program, List[Diagnostic]]:
    state = ParsingState(code=code, tokens=tokens, position=0)
    diagnostics: List[Diagnostic] = []

    snippets: List[tree.snippet.Snippet] = []
    functions: List[tree.function.Function] = []

    try:
        while not state.is_eof():
            match parse_entity(state):
                case tree.snippet.Snippet() as snippet:
                    snippets.append(snippet)
                case tree.function.Function() as function:
                    functions.append(function)

    except UnexpectedEndOfTokens as e:
        diagnostics.append(report_e2000_unexpected_end_of_tokens(e.offset))

    except UnexpectedTokenCode as e:
        diagnostics.append(report_e2001_unexpected_token(e.token, e.expected, e.found))

    except UnexpectedKeyword as e:
        diagnostics.append(
            report_e2002_unexpected_keyword(e.token, e.expected, e.found)
        )

    except FlagAlreadySpecified as e:
        diagnostics.append(report_e2003_flag_already_specified(e.token, e.flag))

    except InvalidHexLiteral as e:
        diagnostics.append(report_e2004_invalid_hex_literal(e.token))

    # any diagnostics stops further processing
    if diagnostics:
        return result.Err(diagnostics)

    return result.Ok(
        tree.Program(
            functions=functions,
            snippets=snippets,
        )
    )


def parse_entity(
    state: ParsingState,
) -> Union[tree.snippet.Snippet, tree.function.Function]:
    expected = {b"asm", b"fn"}
    keyword = state.expect(Tokens.KEYWORD)

    if state.extract(keyword) not in expected:
        raise UnexpectedKeyword(keyword, list(expected), state.extract(keyword))

    if state.extract(keyword) == b"asm":
        return parse_snippet(state)

    else:
        return parse_function(state)


def report_e2000_unexpected_end_of_tokens(offset: int) -> Diagnostic:
    return Diagnostic(
        code="E2000",
        ref=Span(offset=offset, length=0),
        message=f"Unexpected end of tokens at offset {offset}",
    )


def report_e2001_unexpected_token(
    ref: SpanLike, expected: List[int], found: int
) -> Diagnostic:
    found_name = TOKEN_NAMES[found]
    expected_names = [TOKEN_NAMES[token] for token in expected]

    return Diagnostic(
        ref=ref,
        code="E2001",
        message=f"Unexpected token '{found_name}' at offset {ref.offset}, expected one of: {expected_names}",
    )


def report_e2002_unexpected_keyword(
    ref: SpanLike, expected: Union[List[bytes], Set[bytes]], found: bytes
) -> Diagnostic:
    return Diagnostic(
        ref=ref,
        code="E2002",
        message=f"Unexpected keyword '{found.decode()}' at offset {ref.offset}, expected one of: {list(expected)}",
    )


def report_e2003_flag_already_specified(ref: SpanLike, flag: bytes) -> Diagnostic:
    return Diagnostic(
        ref=ref,
        code="E2003",
        message=f"Flag '{flag.decode()}' already specified at offset {ref.offset}",
    )


def report_e2004_invalid_hex_literal(ref: SpanLike) -> Diagnostic:
    return Diagnostic(
        ref=ref,
        code="E2004",
        message=f"Invalid hex literal at offset {ref.offset}",
    )
