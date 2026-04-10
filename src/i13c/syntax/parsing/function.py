from typing import List, Optional

from i13c.syntax import tree
from i13c.syntax.lexing import Token as LexingToken
from i13c.syntax.lexing import Tokens
from i13c.syntax.parsing.core import (
    FlagAlreadySpecified,
    ParsingState,
    UnexpectedKeyword,
    UnexpectedTokenCode,
)
from i13c.syntax.parsing.literals import extract_hex
from i13c.syntax.parsing.types import parse_range


def parse_function(state: ParsingState) -> tree.function.Function:
    statements: List[tree.function.Statement] = []
    parameters: List[tree.function.Parameter] = []
    noreturn: bool = False

    # function name is an identifier
    name = state.expect(Tokens.IDENT)

    # expect opening round bracket
    state.expect(Tokens.ROUND_OPEN)

    # optional function parameters
    if not state.is_in(Tokens.ROUND_CLOSE):
        parameters = parse_parameters(state)

    # expect closed round bracket
    end = state.expect(Tokens.ROUND_CLOSE)

    # optional flags
    if not state.is_in(Tokens.CURLY_OPEN):
        noreturn = parse_function_flags(state)

    # expect opening curly brace
    state.expect(Tokens.CURLY_OPEN)

    # parse statements until closing curly brace
    while not state.is_in(Tokens.CURLY_CLOSE):
        statements.append(parse_statement(state))

    # expect closed curly brace
    state.expect(Tokens.CURLY_CLOSE)

    return tree.function.Function(
        ref=state.between(name, end),
        name=state.extract(name),
        noreturn=noreturn,
        parameters=parameters,
        statements=statements,
    )


def parse_parameters(state: ParsingState) -> List[tree.function.Parameter]:
    parameters: List[tree.function.Parameter] = []
    parameters.append(parse_parameter(state))

    # a comma suggests next parameter
    while state.accept(Tokens.COMMA):
        parameters.append(parse_parameter(state))

    return parameters


def parse_parameter(state: ParsingState) -> tree.function.Parameter:
    range: Optional[tree.types.Range] = None
    ident = state.expect(Tokens.IDENT)

    # expect ':' followed by type
    state.expect(Tokens.COLON)
    type = state.expect(Tokens.TYPE)

    if state.is_in(Tokens.SQUARE_OPEN):
        range = parse_range(state)

    return tree.function.Parameter(
        ref=state.span(ident),
        name=state.extract(ident),
        type=tree.types.Type(
            ref=state.between(type, type),
            name=state.extract(type),
            range=range,
        ),
    )


def parse_function_flags(state: ParsingState) -> bool:
    keyword: Optional[LexingToken] = None
    terminal = False

    while not state.is_in(Tokens.CURLY_OPEN):
        expected = {b"noreturn"}
        keyword = state.expect(Tokens.KEYWORD)

        # fail if the keyword is not "noreturn"
        if state.extract(keyword) not in expected:
            raise UnexpectedKeyword(keyword, expected, state.extract(keyword))

        # if "noreturn", set terminal flag
        elif state.extract(keyword) == b"noreturn":
            if terminal:
                raise FlagAlreadySpecified(keyword, b"noreturn")
            else:
                terminal = True

    return terminal


def parse_statement(state: ParsingState) -> tree.function.Statement:
    token = state.expect(Tokens.IDENT, Tokens.KEYWORD)

    if token.code == Tokens.IDENT:
        return parse_callsite(state, token)

    if state.extract(token) == b"val":
        return parse_value(state)

    raise UnexpectedTokenCode(token, [Tokens.IDENT, Tokens.KEYWORD], token.code)


def parse_callsite(
    state: ParsingState, ident: LexingToken
) -> tree.function.CallStatement:
    arguments: List[tree.function.Argument] = []

    # expect opening round bracket
    state.expect(Tokens.ROUND_OPEN)

    # optional arguments
    if state.is_in(Tokens.HEX, Tokens.IDENT):
        arguments = parse_arguments(state)

    # expect closed round bracket
    end = state.expect(Tokens.ROUND_CLOSE)

    # expect a semicolon
    state.expect(Tokens.SEMICOLON)

    return tree.function.CallStatement(
        ref=state.between(ident, end),
        name=state.extract(ident),
        arguments=arguments,
    )


def parse_value(state: ParsingState) -> tree.function.ValueStatement:
    range: Optional[tree.types.Range] = None
    ident = state.expect(Tokens.IDENT)

    # expect ':' followed by type
    state.expect(Tokens.COLON)
    type = state.expect(Tokens.TYPE)

    if state.is_in(Tokens.SQUARE_OPEN):
        range = parse_range(state)

    # expect '=' followed by limited expression
    state.expect(Tokens.EQUALS)
    expression = parse_value_expression(state)

    # expect a semicolon
    state.expect(Tokens.SEMICOLON)

    return tree.function.ValueStatement(
        ref=state.span(ident),
        name=state.extract(ident),
        type=tree.types.Type(
            ref=state.between(type, type),
            name=state.extract(type),
            range=range,
        ),
        expr=expression,
    )


def parse_value_expression(state: ParsingState) -> tree.function.ValueExpression:
    return parse_argument(state)


def parse_arguments(state: ParsingState) -> List[tree.function.Argument]:
    arguments: List[tree.function.Argument] = []
    arguments.append(parse_argument(state))

    # a comma suggests next argument
    while state.accept(Tokens.COMMA):
        arguments.append(parse_argument(state))

    return arguments


def parse_argument(state: ParsingState) -> tree.function.Argument:
    token = state.expect(Tokens.HEX, Tokens.IDENT)

    # a hex can be only an integer literal
    if token.code == Tokens.HEX:
        return tree.function.IntegerLiteral(
            ref=state.span(token),
            value=extract_hex(state, token),
        )

    # an identifier can be only an expression
    return tree.function.Expression(
        ref=state.span(token),
        name=state.extract(token),
    )
