from dataclasses import dataclass
from typing import List, Union

from i13c import ast, diag, lex, res, src


class UnexpectedTokenCode(Exception):
    def __init__(self, offset: int, expected: List[int], found: int) -> None:
        self.offset = offset
        self.expected = expected
        self.found = found


class UnexpectedEndOfTokens(Exception):
    def __init__(self, offset: int) -> None:
        self.offset = offset


class UnexpectedKeyword(Exception):
    def __init__(self, offset: int, expected: List[bytes], found: bytes) -> None:
        self.offset = offset
        self.expected = expected
        self.found = found


@dataclass(kw_only=True)
class ParsingState:
    code: src.SourceCode
    tokens: List[lex.Token]
    position: int

    def is_eof(self) -> bool:
        return self.tokens[self.position].code == lex.TOKEN_EOF

    def is_in(self, *codes: int) -> bool:
        return self.tokens[self.position].code in codes

    def span(self, token: lex.Token) -> ast.Span:
        return ast.Span(
            offset=token.offset,
            length=self.tokens[self.position].length - token.offset,
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
                self.tokens[self.position].offset,
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
    functions: List[ast.Function] = []

    try:
        while not state.is_eof():
            functions.append(parse_function(state))

    except UnexpectedEndOfTokens as e:
        diagnostics.append(report_unexpected_end_of_tokens(e.offset))

    except UnexpectedTokenCode as e:
        diagnostics.append(report_unexpected_token(e.offset, e.expected, e.found))

    except UnexpectedKeyword as e:
        diagnostics.append(report_unexpected_keyword(e.offset, e.expected, e.found))

    # any diagnostics stops further processing
    if diagnostics:
        return res.Err(diagnostics)

    return res.Ok(ast.Program(functions=functions))


def parse_function(state: ParsingState) -> ast.Function:
    instructions: List[ast.Instruction] = []
    parameters: List[ast.Parameter] = []
    clobbers: List[ast.Register] = []

    # currently only "asm" functions are supported
    keyword = state.expect(lex.TOKEN_KEYWORD)

    if state.extract(keyword) != b"asm":
        raise UnexpectedKeyword(keyword.offset, [b"asm"], state.extract(keyword))

    # function name is an identifier
    name = state.expect(lex.TOKEN_IDENT)

    # expect opening round bracket
    state.expect(lex.TOKEN_ROUND_OPEN)

    # optional function parameters
    while not state.is_in(lex.TOKEN_ROUND_CLOSE):
        parameters = parse_parameters(state)

    # expect closed round bracket
    state.expect(lex.TOKEN_ROUND_CLOSE)

    # capture function signature
    ref = state.span(name)

    # optional clobbers
    while not state.is_in(lex.TOKEN_CURLY_OPEN):
        clobbers = parse_clobbers(state)

    # expect opening curly brace
    state.expect(lex.TOKEN_CURLY_OPEN)

    # parse instructions until closing curly brace
    while not state.is_in(lex.TOKEN_CURLY_CLOSE):
        instructions.append(parse_instruction(state))

    # expect closed curly brace
    state.expect(lex.TOKEN_CURLY_CLOSE)

    return ast.Function(
        ref=ref,
        name=state.extract(name),
        clobbers=clobbers,
        parameters=parameters,
        instructions=instructions,
    )


def parse_parameters(state: ParsingState) -> List[ast.Parameter]:
    parameters: List[ast.Parameter] = []
    parameters.append(parse_parameter(state))

    # a comma suggests next parameter
    while state.accept(lex.TOKEN_COMMA):
        parameters.append(parse_parameter(state))

    return parameters


def parse_parameter(state: ParsingState) -> ast.Parameter:
    ident = state.expect(lex.TOKEN_IDENT)

    # expect '@' followed by register
    state.expect(lex.TOKEN_AT)
    bind = state.expect(lex.TOKEN_REG)

    # expect ':' followed by type
    state.expect(lex.TOKEN_COLON)
    type = state.expect(lex.TOKEN_TYPE)

    return ast.Parameter(
        name=state.extract(ident),
        type=ast.Type(name=state.extract(type)),
        bind=ast.Register(name=state.extract(bind)),
    )


def parse_clobbers(state: ParsingState) -> List[ast.Register]:
    clobbers: List[ast.Register] = []
    keyword = state.expect(lex.TOKEN_KEYWORD)

    # fail if the keyword is not "clobbers"
    if state.extract(keyword) != b"clobbers":
        raise UnexpectedKeyword(keyword.offset, [b"clobbers"], state.extract(keyword))

    # at least one register is expected
    clobber = state.expect(lex.TOKEN_REG)
    clobbers.append(ast.Register(name=state.extract(clobber)))

    # a comma suggests next clobber
    while state.accept(lex.TOKEN_COMMA):
        clobber = state.expect(lex.TOKEN_REG)
        clobbers.append(ast.Register(name=state.extract(clobber)))

    return clobbers


def parse_instruction(state: ParsingState) -> ast.Instruction:
    operands = []
    token = state.expect(lex.TOKEN_MNEMONIC)

    # optional operands
    if state.is_in(lex.TOKEN_REG, lex.TOKEN_HEX):
        operands = parse_operands(state)

    # expect a semicolon
    state.expect(lex.TOKEN_SEMICOLON)

    # build instruction and token reference
    ref = state.span(token)
    mnemonic = ast.Mnemonic(name=state.extract(token))

    return ast.Instruction(ref=ref, mnemonic=mnemonic, operands=operands)


def parse_operands(state: ParsingState) -> List[Union[ast.Register, ast.Immediate]]:
    operands: List[Union[ast.Register, ast.Immediate]] = []
    operands.append(parse_operand(state))

    # a comma suggests next operand
    while state.accept(lex.TOKEN_COMMA):
        operands.append(parse_operand(state))

    return operands


def parse_operand(state: ParsingState) -> Union[ast.Register, ast.Immediate]:
    token = state.expect(lex.TOKEN_REG, lex.TOKEN_HEX)

    # register has to provide its name
    if token.code == lex.TOKEN_REG:
        return ast.Register(name=state.extract(token))

    # immediate has to provide its decimal value
    else:
        return ast.Immediate(value=int(state.extract(token), 16))


def report_unexpected_end_of_tokens(offset: int) -> diag.Diagnostic:
    return diag.Diagnostic(
        offset=offset,
        code="P001",
        message=f"Unexpected end of tokens at offset {offset}",
    )


def report_unexpected_token(
    offset: int, expected: List[int], found: int
) -> diag.Diagnostic:
    return diag.Diagnostic(
        offset=offset,
        code="P002",
        message=f"Unexpected token code {found} at offset {offset}, expected one of: {list(expected)}",
    )


def report_unexpected_keyword(
    offset: int, expected: List[bytes], found: bytes
) -> diag.Diagnostic:
    return diag.Diagnostic(
        offset=offset,
        code="P003",
        message=f"Unexpected keyword '{found.decode()}' at offset {offset}, expected one of: {list(expected)}",
    )
