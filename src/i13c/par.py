from dataclasses import dataclass
from typing import List, Optional, Set, Tuple, Union

from i13c import ast, diag, err, lex, res, src


class UnexpectedTokenCode(Exception):
    def __init__(self, token: lex.Token, expected: List[int], found: int) -> None:
        self.token = token
        self.expected = expected
        self.found = found


class UnexpectedEndOfTokens(Exception):
    def __init__(self, offset: int) -> None:
        self.offset = offset


class UnexpectedKeyword(Exception):
    def __init__(
        self, token: lex.Token, expected: Union[List[bytes], Set[bytes]], found: bytes
    ) -> None:
        self.token = token
        self.expected = expected
        self.found = found


class FlagAlreadySpecified(Exception):
    def __init__(self, token: lex.Token, flag: bytes) -> None:
        self.token = token
        self.flag = flag


@dataclass(kw_only=True)
class ParsingState:
    code: src.SourceCode
    tokens: List[lex.Token]
    position: int

    def is_eof(self) -> bool:
        return self.tokens[self.position].code == lex.TOKEN_EOF

    def is_in(self, *codes: int) -> bool:
        return self.tokens[self.position].code in codes

    def span(self, token: lex.Token) -> src.Span:
        return src.Span(
            offset=token.offset,
            length=self.tokens[self.position].offset - token.offset,
        )

    def between(self, left: lex.Token, right: lex.Token) -> src.Span:
        return src.Span(
            offset=left.offset,
            length=right.offset + right.length - left.offset,
        )

    def accept(self, *codes: int) -> bool:
        if self.is_in(*codes):
            self.advance()
            return True

        else:
            return False

    def expect(self, *codes: int) -> lex.Token:
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

    def extract(self, token: lex.Token) -> bytes:
        return self.code.extract(token)


def parse(
    code: src.SourceCode, tokens: List[lex.Token]
) -> res.Result[ast.Program, List[diag.Diagnostic]]:
    state = ParsingState(code=code, tokens=tokens, position=0)
    diagnostics: List[diag.Diagnostic] = []

    snippets: List[ast.Snippet] = []
    functions: List[ast.Function] = []

    try:
        while not state.is_eof():
            match parse_entity(state):
                case ast.Snippet() as snippet:
                    snippets.append(snippet)
                case ast.Function() as function:
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
        ast.Program(
            functions=functions,
            snippets=snippets,
        )
    )


def parse_entity(state: ParsingState) -> Union[ast.Snippet, ast.Function]:
    expected = {b"asm", b"fn"}
    keyword = state.expect(lex.TOKEN_KEYWORD)

    if state.extract(keyword) not in expected:
        raise UnexpectedKeyword(keyword, list(expected), state.extract(keyword))

    if state.extract(keyword) == b"asm":
        return parse_snippet(state)

    else:
        return parse_function(state)


def parse_function(state: ParsingState) -> ast.Function:
    statements: List[ast.CallStatement] = []
    parameters: List[ast.Parameter] = []
    noreturn: bool = False

    # function name is an identifier
    name = state.expect(lex.TOKEN_IDENT)

    # expect opening round bracket
    state.expect(lex.TOKEN_ROUND_OPEN)

    # optional function parameters
    if not state.is_in(lex.TOKEN_ROUND_CLOSE):
        parameters = parse_parameters(state)

    # expect closed round bracket
    end = state.expect(lex.TOKEN_ROUND_CLOSE)

    # optional flags
    if not state.is_in(lex.TOKEN_CURLY_OPEN):
        noreturn = parse_function_flags(state)

    # expect opening curly brace
    state.expect(lex.TOKEN_CURLY_OPEN)

    # parse statements until closing curly brace
    while not state.is_in(lex.TOKEN_CURLY_CLOSE):
        statements.append(parse_statement(state))

    # expect closed curly brace
    state.expect(lex.TOKEN_CURLY_CLOSE)

    return ast.Function(
        ref=state.between(name, end),
        name=state.extract(name),
        noreturn=noreturn,
        parameters=parameters,
        statements=statements,
    )


def parse_snippet(state: ParsingState) -> ast.Snippet:
    instructions: List[ast.Instruction] = []
    slots: List[ast.Slot] = []
    clobbers: List[ast.Register] = []
    noreturn: bool = False

    # snippet name is an identifier
    name = state.expect(lex.TOKEN_IDENT)

    # expect opening round bracket
    state.expect(lex.TOKEN_ROUND_OPEN)

    # optional snippet parameters
    if not state.is_in(lex.TOKEN_ROUND_CLOSE):
        slots = parse_slots(state)

    # expect closed round bracket
    end = state.expect(lex.TOKEN_ROUND_CLOSE)

    # optional flags
    if not state.is_in(lex.TOKEN_CURLY_OPEN):
        clobbers, noreturn = parse_snippet_flags(state)

    # expect opening curly brace
    state.expect(lex.TOKEN_CURLY_OPEN)

    # parse instructions until closing curly brace
    while not state.is_in(lex.TOKEN_CURLY_CLOSE):
        instructions.append(parse_instruction(state))

    # expect closed curly brace
    state.expect(lex.TOKEN_CURLY_CLOSE)

    return ast.Snippet(
        ref=state.between(name, end),
        name=state.extract(name),
        noreturn=noreturn,
        clobbers=clobbers,
        slots=slots,
        instructions=instructions,
    )


def parse_parameters(state: ParsingState) -> List[ast.Parameter]:
    parameters: List[ast.Parameter] = []
    parameters.append(parse_parameter(state))

    # a comma suggests next parameter
    while state.accept(lex.TOKEN_COMMA):
        parameters.append(parse_parameter(state))

    return parameters


def parse_slots(state: ParsingState) -> List[ast.Slot]:
    parameters: List[ast.Slot] = []
    parameters.append(parse_slot(state))

    # a comma suggests next parameter
    while state.accept(lex.TOKEN_COMMA):
        parameters.append(parse_slot(state))

    return parameters


def parse_parameter(state: ParsingState) -> ast.Parameter:
    ident = state.expect(lex.TOKEN_IDENT)

    # expect ':' followed by type
    state.expect(lex.TOKEN_COLON)
    type = state.expect(lex.TOKEN_TYPE)

    return ast.Parameter(
        name=state.extract(ident),
        type=ast.Type(name=state.extract(type)),
    )


def parse_slot(state: ParsingState) -> ast.Slot:
    ident = state.expect(lex.TOKEN_IDENT)

    # expect '@' followed by register
    state.expect(lex.TOKEN_AT)
    bind = state.expect(lex.TOKEN_REG)

    # expect ':' followed by type
    state.expect(lex.TOKEN_COLON)
    type = state.expect(lex.TOKEN_TYPE)

    return ast.Slot(
        name=state.extract(ident),
        type=ast.Type(name=state.extract(type)),
        bind=ast.Register(name=state.extract(bind)),
    )


def parse_function_flags(state: ParsingState) -> bool:
    keyword: Optional[lex.Token] = None
    terminal = False

    while not state.is_in(lex.TOKEN_CURLY_OPEN):
        expected = {b"noreturn"}
        keyword = state.expect(lex.TOKEN_KEYWORD)

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


def parse_snippet_flags(state: ParsingState) -> Tuple[List[ast.Register], bool]:
    keyword: Optional[lex.Token] = None
    clobbers: Optional[List[ast.Register]] = None
    terminal = False

    while not state.is_in(lex.TOKEN_CURLY_OPEN):
        expected = {b"clobbers", b"noreturn"}
        keyword = state.expect(lex.TOKEN_KEYWORD)

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


def parse_clobbers(state: ParsingState) -> List[ast.Register]:
    clobbers: List[ast.Register] = []

    # at least one register is expected
    clobber = state.expect(lex.TOKEN_REG)
    clobbers.append(ast.Register(name=state.extract(clobber)))

    # a comma suggests next clobber
    while state.accept(lex.TOKEN_COMMA):
        clobber = state.expect(lex.TOKEN_REG)
        clobbers.append(ast.Register(name=state.extract(clobber)))

    return clobbers


def parse_statement(state: ParsingState) -> ast.CallStatement:
    arguments = []
    ident = state.expect(lex.TOKEN_IDENT)

    # expect opening round bracket
    state.expect(lex.TOKEN_ROUND_OPEN)

    # optional arguments
    if state.is_in(lex.TOKEN_HEX):
        arguments = parse_arguments(state)

    # expect closed round bracket
    end = state.expect(lex.TOKEN_ROUND_CLOSE)

    # expect a semicolon
    state.expect(lex.TOKEN_SEMICOLON)

    return ast.CallStatement(
        ref=state.between(ident, end),
        name=state.extract(ident),
        arguments=arguments,
    )


def parse_instruction(state: ParsingState) -> ast.Instruction:
    operands = []
    token = state.expect(lex.TOKEN_MNEMONIC)

    # optional operands
    if state.is_in(lex.TOKEN_REG, lex.TOKEN_HEX):
        operands = parse_operands(state)

    # expect a semicolon
    end = state.expect(lex.TOKEN_SEMICOLON)

    # build instruction and token reference
    mnemonic = ast.Mnemonic(name=state.extract(token))

    return ast.Instruction(
        ref=state.between(token, end),
        mnemonic=mnemonic,
        operands=operands,
    )


def parse_arguments(state: ParsingState) -> List[ast.IntegerLiteral]:
    arguments: List[ast.IntegerLiteral] = []
    arguments.append(parse_argument(state))

    # a comma suggests next argument
    while state.accept(lex.TOKEN_COMMA):
        arguments.append(parse_argument(state))

    return arguments


def parse_operands(state: ParsingState) -> List[Union[ast.Register, ast.Immediate]]:
    operands: List[Union[ast.Register, ast.Immediate]] = []
    operands.append(parse_operand(state))

    # a comma suggests next operand
    while state.accept(lex.TOKEN_COMMA):
        operands.append(parse_operand(state))

    return operands


def parse_argument(state: ParsingState) -> ast.IntegerLiteral:
    token = state.expect(lex.TOKEN_HEX)

    return ast.IntegerLiteral(
        ref=state.span(token),
        value=int(state.extract(token), 16),
    )


def parse_operand(state: ParsingState) -> Union[ast.Register, ast.Immediate]:
    token = state.expect(lex.TOKEN_REG, lex.TOKEN_HEX)

    # register has to provide its name
    if token.code == lex.TOKEN_REG:
        return ast.Register(name=state.extract(token))

    # immediate has to provide its decimal value
    else:
        return ast.Immediate(value=int(state.extract(token), 16))
