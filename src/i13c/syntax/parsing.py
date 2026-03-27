from dataclasses import dataclass
from typing import List, Optional, Set, Tuple, Union

from i13c import err, res
from i13c.core import diagnostics
from i13c.syntax import tree
from i13c.syntax.lexing import Token as LexingToken
from i13c.syntax.lexing import Tokens
from i13c.syntax.source import SourceCode, Span


class UnexpectedTokenCode(Exception):
    def __init__(self, token: LexingToken, expected: List[int], found: int) -> None:
        self.token = token
        self.expected = expected
        self.found = found


class UnexpectedEndOfTokens(Exception):
    def __init__(self, offset: int) -> None:
        self.offset = offset


class UnexpectedKeyword(Exception):
    def __init__(
        self, token: LexingToken, expected: Union[List[bytes], Set[bytes]], found: bytes
    ) -> None:
        self.token = token
        self.expected = expected
        self.found = found


class FlagAlreadySpecified(Exception):
    def __init__(self, token: LexingToken, flag: bytes) -> None:
        self.token = token
        self.flag = flag


@dataclass(kw_only=True)
class ParsingState:
    code: SourceCode
    tokens: List[LexingToken]
    position: int

    def is_eof(self) -> bool:
        return self.tokens[self.position].code == Tokens.EOF

    def is_in(self, *codes: int) -> bool:
        return self.tokens[self.position].code in codes

    def span(self, token: LexingToken) -> Span:
        return Span(
            offset=token.offset,
            length=token.length,
        )

    def between(self, left: LexingToken, right: LexingToken) -> Span:
        return Span(
            offset=left.offset,
            length=right.offset + right.length - left.offset,
        )

    def accept(self, *codes: int) -> bool:
        if self.is_in(*codes):
            self.advance()
            return True

        else:
            return False

    def expect(self, *codes: int) -> LexingToken:
        if self.is_eof():
            raise UnexpectedEndOfTokens(self.tokens[self.position].offset)

        if self.tokens[self.position].code not in codes:
            raise UnexpectedTokenCode(
                self.tokens[self.position],
                list(codes),
                self.tokens[self.position].code,
            )

        # consume token
        self.advance()

        # return the consumed token
        return self.tokens[self.position - 1]

    def advance(self) -> None:
        self.position += 1

    def extract(self, token: LexingToken) -> bytes:
        return self.code.extract(token)


def parse(
    code: SourceCode, tokens: List[LexingToken]
) -> res.Result[tree.Program, List[diagnostics.Diagnostic]]:
    state = ParsingState(code=code, tokens=tokens, position=0)
    diagnostics: List[diagnostics.Diagnostic] = []

    snippets: List[tree.Snippet] = []
    functions: List[tree.Function] = []

    try:
        while not state.is_eof():
            match parse_entity(state):
                case tree.Snippet() as snippet:
                    snippets.append(snippet)
                case tree.Function() as function:
                    functions.append(function)

    except UnexpectedEndOfTokens as e:
        diagnostics.append(err.report_e2000_unexpected_end_of_tokens(e.offset))

    except UnexpectedTokenCode as e:
        diagnostics.append(
            err.report_e2001_unexpected_token(e.token, e.expected, e.found)
        )

    except UnexpectedKeyword as e:
        diagnostics.append(
            err.report_e2002_unexpected_keyword(e.token, e.expected, e.found)
        )

    except FlagAlreadySpecified as e:
        diagnostics.append(err.report_e2003_flag_already_specified(e.token, e.flag))

    # any diagnostics stops further processing
    if diagnostics:
        return res.Err(diagnostics)

    return res.Ok(
        tree.Program(
            functions=functions,
            snippets=snippets,
        )
    )


def parse_entity(state: ParsingState) -> Union[tree.Snippet, tree.Function]:
    expected = {b"asm", b"fn"}
    keyword = state.expect(Tokens.KEYWORD)

    if state.extract(keyword) not in expected:
        raise UnexpectedKeyword(keyword, list(expected), state.extract(keyword))

    if state.extract(keyword) == b"asm":
        return parse_snippet(state)

    else:
        return parse_function(state)


def parse_function(state: ParsingState) -> tree.Function:
    statements: List[tree.Statement] = []
    parameters: List[tree.Parameter] = []
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

    return tree.Function(
        ref=state.between(name, end),
        name=state.extract(name),
        noreturn=noreturn,
        parameters=parameters,
        statements=statements,
    )


def parse_snippet(state: ParsingState) -> tree.Snippet:
    instructions: List[tree.Instruction] = []
    slots: List[tree.Slot] = []
    clobbers: List[tree.Register] = []
    noreturn: bool = False

    # snippet name is an identifier
    name = state.expect(Tokens.IDENT)

    # expect opening round bracket
    state.expect(Tokens.ROUND_OPEN)

    # optional snippet parameters
    if not state.is_in(Tokens.ROUND_CLOSE):
        slots = parse_slots(state)

    # expect closed round bracket
    end = state.expect(Tokens.ROUND_CLOSE)

    # optional flags
    if not state.is_in(Tokens.CURLY_OPEN):
        clobbers, noreturn = parse_snippet_flags(state)

    # expect opening curly brace
    state.expect(Tokens.CURLY_OPEN)

    # parse instructions until closing curly brace
    while not state.is_in(Tokens.CURLY_CLOSE):
        instructions.append(parse_instruction(state))

    # expect closed curly brace
    state.expect(Tokens.CURLY_CLOSE)

    return tree.Snippet(
        ref=state.between(name, end),
        name=state.extract(name),
        noreturn=noreturn,
        clobbers=clobbers,
        slots=slots,
        instructions=instructions,
    )


def parse_parameters(state: ParsingState) -> List[tree.Parameter]:
    parameters: List[tree.Parameter] = []
    parameters.append(parse_parameter(state))

    # a comma suggests next parameter
    while state.accept(Tokens.COMMA):
        parameters.append(parse_parameter(state))

    return parameters


def parse_slots(state: ParsingState) -> List[tree.Slot]:
    parameters: List[tree.Slot] = []
    parameters.append(parse_slot(state))

    # a comma suggests next parameter
    while state.accept(Tokens.COMMA):
        parameters.append(parse_slot(state))

    return parameters


def parse_parameter(state: ParsingState) -> tree.Parameter:
    range: Optional[tree.Range] = None
    ident = state.expect(Tokens.IDENT)

    # expect ':' followed by type
    state.expect(Tokens.COLON)
    type = state.expect(Tokens.TYPE)

    if state.is_in(Tokens.SQUARE_OPEN):
        range = parse_range(state)

    return tree.Parameter(
        ref=state.span(ident),
        name=state.extract(ident),
        type=tree.Type(name=state.extract(type), range=range),
    )


def parse_slot(state: ParsingState) -> tree.Slot:
    range: Optional[tree.Range] = None
    ident = state.expect(Tokens.IDENT)

    # expect '@' followed by register or immediate
    state.expect(Tokens.AT)
    bind = state.expect(Tokens.REG, Tokens.KEYWORD)

    # if it's a keyword, it has to be "imm"
    if bind.code == Tokens.KEYWORD:
        if state.extract(bind) != b"imm":
            raise UnexpectedKeyword(bind, [b"imm"], state.extract(bind))

    # expect ':' followed by type
    state.expect(Tokens.COLON)
    type = state.expect(Tokens.TYPE)

    if state.is_in(Tokens.SQUARE_OPEN):
        range = parse_range(state)

    return tree.Slot(
        name=state.extract(ident),
        bind=tree.Binding(name=state.extract(bind)),
        type=tree.Type(name=state.extract(type), range=range),
    )


def parse_range(state: ParsingState) -> tree.Range:
    # expect opening square bracket
    state.expect(Tokens.SQUARE_OPEN)
    lower = state.expect(Tokens.HEX)

    # expect range operator
    state.expect(Tokens.RANGE)
    upper = state.expect(Tokens.HEX)

    # expect closing square bracket
    state.expect(Tokens.SQUARE_CLOSE)

    return tree.Range(
        lower=int(state.extract(lower), 16),
        upper=int(state.extract(upper), 16),
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


def parse_snippet_flags(state: ParsingState) -> Tuple[List[tree.Register], bool]:
    keyword: Optional[LexingToken] = None
    clobbers: Optional[List[tree.Register]] = None
    terminal = False

    while not state.is_in(Tokens.CURLY_OPEN):
        expected = {b"clobbers", b"noreturn"}
        keyword = state.expect(Tokens.KEYWORD)

        # fail if the keyword is not "noreturn"
        if state.extract(keyword) not in expected:
            raise UnexpectedKeyword(keyword, expected, state.extract(keyword))

        # if "clobbers", parse the clobber list
        if state.extract(keyword) == b"clobbers":
            if clobbers is not None:
                raise FlagAlreadySpecified(keyword, b"clobbers")
            else:
                clobbers = parse_clobbers(state)

        # if "noreturn", set terminal flag
        elif state.extract(keyword) == b"noreturn":
            if terminal:
                raise FlagAlreadySpecified(keyword, b"noreturn")
            else:
                terminal = True

    return clobbers or [], terminal


def parse_clobbers(state: ParsingState) -> List[tree.Register]:
    clobbers: List[tree.Register] = []

    # at least one register is expected
    clobber = state.expect(Tokens.REG)
    clobbers.append(tree.Register(ref=state.span(clobber), name=state.extract(clobber)))

    # a comma suggests next clobber
    while state.accept(Tokens.COMMA):
        clobber = state.expect(Tokens.REG)
        clobbers.append(
            tree.Register(ref=state.span(clobber), name=state.extract(clobber))
        )

    return clobbers


def parse_statement(state: ParsingState) -> tree.Statement:
    token = state.expect(Tokens.IDENT, Tokens.KEYWORD)

    if token.code == Tokens.IDENT:
        return parse_callsite(state, token)

    if state.extract(token) == b"val":
        return parse_value(state)

    raise UnexpectedTokenCode(token, [Tokens.IDENT, Tokens.KEYWORD], token.code)


def parse_callsite(state: ParsingState, ident: LexingToken) -> tree.CallStatement:
    arguments: List[tree.Argument] = []

    # expect opening round bracket
    state.expect(Tokens.ROUND_OPEN)

    # optional arguments
    if state.is_in(Tokens.HEX, Tokens.IDENT):
        arguments = parse_arguments(state)

    # expect closed round bracket
    end = state.expect(Tokens.ROUND_CLOSE)

    # expect a semicolon
    state.expect(Tokens.SEMICOLON)

    return tree.CallStatement(
        ref=state.between(ident, end),
        name=state.extract(ident),
        arguments=arguments,
    )


def parse_value(state: ParsingState) -> tree.ValueStatement:
    range: Optional[tree.Range] = None
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

    return tree.ValueStatement(
        ref=state.span(ident),
        name=state.extract(ident),
        type=tree.Type(name=state.extract(type), range=range),
        expr=expression,
    )


def parse_value_expression(state: ParsingState) -> tree.ValueExpression:
    return parse_argument(state)


def parse_instruction(state: ParsingState) -> tree.Instruction:
    operands: List[tree.Operand] = []
    token = state.expect(Tokens.IDENT)

    # optional operands
    if state.is_in(Tokens.REG, Tokens.HEX, Tokens.IDENT):
        operands = parse_operands(state)

    # expect a semicolon
    end = state.expect(Tokens.SEMICOLON)

    # build instruction and token reference
    mnemonic = tree.Mnemonic(name=state.extract(token))

    return tree.Instruction(
        ref=state.between(token, end),
        mnemonic=mnemonic,
        operands=operands,
    )


def parse_arguments(state: ParsingState) -> List[tree.Argument]:
    arguments: List[tree.Argument] = []
    arguments.append(parse_argument(state))

    # a comma suggests next argument
    while state.accept(Tokens.COMMA):
        arguments.append(parse_argument(state))

    return arguments


def parse_operands(state: ParsingState) -> List[tree.Operand]:
    operands: List[tree.Operand] = []
    operands.append(parse_operand(state))

    # a comma suggests next operand
    while state.accept(Tokens.COMMA):
        operands.append(parse_operand(state))

    return operands


def parse_argument(state: ParsingState) -> tree.Argument:
    token = state.expect(Tokens.HEX, Tokens.IDENT)

    # a hex can be only an integer literal
    if token.code == Tokens.HEX:
        return tree.IntegerLiteral(
            ref=state.span(token),
            value=int(state.extract(token), 16),
        )

    # an identifier can be only an expression
    return tree.Expression(
        ref=state.span(token),
        name=state.extract(token),
    )


def parse_operand(state: ParsingState) -> tree.Operand:
    token = state.expect(Tokens.REG, Tokens.HEX, Tokens.IDENT)

    # register has to provide its name
    if token.code == Tokens.REG:
        return tree.Register(ref=state.span(token), name=state.extract(token))

    # immediate has to provide its decimal value
    elif token.code == Tokens.HEX:
        return tree.Immediate(ref=state.span(token), value=int(state.extract(token), 16))

    # reference has to provide its identifier
    else:
        return tree.Reference(ref=state.span(token), name=state.extract(token))
