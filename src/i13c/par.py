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
    functions: List[Union[ast.AsmFunction, ast.RegFunction]] = []

    try:
        while not state.is_eof():
            functions.append(parse_function(state))

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

    return res.Ok(ast.Program(functions=functions))


def parse_function(state: ParsingState) -> Union[ast.AsmFunction, ast.RegFunction]:
    expected = {b"asm", b"fn"}
    keyword = state.expect(lex.TOKEN_KEYWORD)

    if state.extract(keyword) not in expected:
        raise UnexpectedKeyword(keyword, list(expected), state.extract(keyword))

    if state.extract(keyword) == b"asm":
        return parse_asm_function(state)

    else:
        return parse_reg_function(state)


def parse_reg_function(state: ParsingState) -> ast.RegFunction:
    statements: List[ast.CallStatement] = []
    parameters: List[ast.RegParameter] = []
    terminal: bool = False

    # function name is an identifier
    name = state.expect(lex.TOKEN_IDENT)

    # expect opening round bracket
    state.expect(lex.TOKEN_ROUND_OPEN)

    # optional function parameters
    while not state.is_in(lex.TOKEN_ROUND_CLOSE):
        parameters = parse_reg_parameters(state)

    # expect closed round bracket
    state.expect(lex.TOKEN_ROUND_CLOSE)

    # capture function signature
    ref = state.span(name)

    # optional flags
    if not state.is_in(lex.TOKEN_CURLY_OPEN):
        terminal = parse_reg_function_flags(state)

    # expect opening curly brace
    state.expect(lex.TOKEN_CURLY_OPEN)

    # parse statements until closing curly brace
    while not state.is_in(lex.TOKEN_CURLY_CLOSE):
        statements.append(parse_statement(state))

    # expect closed curly brace
    state.expect(lex.TOKEN_CURLY_CLOSE)

    return ast.RegFunction(
        ref=ref,
        name=state.extract(name),
        terminal=terminal,
        parameters=parameters,
        statements=statements,
    )


def parse_asm_function(state: ParsingState) -> ast.AsmFunction:
    instructions: List[ast.Instruction] = []
    parameters: List[ast.AsmParameter] = []
    clobbers: List[ast.Register] = []
    terminal: bool = False

    # function name is an identifier
    name = state.expect(lex.TOKEN_IDENT)

    # expect opening round bracket
    state.expect(lex.TOKEN_ROUND_OPEN)

    # optional function parameters
    while not state.is_in(lex.TOKEN_ROUND_CLOSE):
        parameters = parse_asm_parameters(state)

    # expect closed round bracket
    state.expect(lex.TOKEN_ROUND_CLOSE)

    # capture function signature
    ref = state.span(name)

    # optional flags
    if not state.is_in(lex.TOKEN_CURLY_OPEN):
        clobbers, terminal = parse_asm_function_flags(state)

    # expect opening curly brace
    state.expect(lex.TOKEN_CURLY_OPEN)

    # parse instructions until closing curly brace
    while not state.is_in(lex.TOKEN_CURLY_CLOSE):
        instructions.append(parse_instruction(state))

    # expect closed curly brace
    state.expect(lex.TOKEN_CURLY_CLOSE)

    return ast.AsmFunction(
        ref=ref,
        name=state.extract(name),
        terminal=terminal,
        clobbers=clobbers,
        parameters=parameters,
        instructions=instructions,
    )


def parse_reg_parameters(state: ParsingState) -> List[ast.RegParameter]:
    parameters: List[ast.RegParameter] = []
    parameters.append(parse_reg_parameter(state))

    # a comma suggests next parameter
    while state.accept(lex.TOKEN_COMMA):
        parameters.append(parse_reg_parameter(state))

    return parameters


def parse_asm_parameters(state: ParsingState) -> List[ast.AsmParameter]:
    parameters: List[ast.AsmParameter] = []
    parameters.append(parse_asm_parameter(state))

    # a comma suggests next parameter
    while state.accept(lex.TOKEN_COMMA):
        parameters.append(parse_asm_parameter(state))

    return parameters


def parse_reg_parameter(state: ParsingState) -> ast.RegParameter:
    ident = state.expect(lex.TOKEN_IDENT)

    # expect ':' followed by type
    state.expect(lex.TOKEN_COLON)
    type = state.expect(lex.TOKEN_TYPE)

    return ast.RegParameter(
        name=state.extract(ident),
        type=ast.Type(name=state.extract(type)),
    )


def parse_asm_parameter(state: ParsingState) -> ast.AsmParameter:
    ident = state.expect(lex.TOKEN_IDENT)

    # expect '@' followed by register
    state.expect(lex.TOKEN_AT)
    bind = state.expect(lex.TOKEN_REG)

    # expect ':' followed by type
    state.expect(lex.TOKEN_COLON)
    type = state.expect(lex.TOKEN_TYPE)

    return ast.AsmParameter(
        name=state.extract(ident),
        type=ast.Type(name=state.extract(type)),
        bind=ast.Register(name=state.extract(bind)),
    )


def parse_reg_function_flags(state: ParsingState) -> bool:
    keyword: Optional[lex.Token] = None
    terminal = False

    while not state.is_in(lex.TOKEN_CURLY_OPEN):
        expected = {b"noreturn"}
        keyword = state.expect(lex.TOKEN_KEYWORD)

        # fail if the keyword is not "clobbers" or "noreturn"
        if state.extract(keyword) not in expected:
            raise UnexpectedKeyword(keyword, expected, state.extract(keyword))

        # if "noreturn", set terminal flag
        elif state.extract(keyword) == b"noreturn":
            if terminal:
                raise FlagAlreadySpecified(keyword, b"noreturn")
            else:
                terminal = True

    return terminal


def parse_asm_function_flags(state: ParsingState) -> Tuple[List[ast.Register], bool]:
    keyword: Optional[lex.Token] = None
    clobbers: Optional[List[ast.Register]] = None
    terminal = False

    while not state.is_in(lex.TOKEN_CURLY_OPEN):
        expected = {b"clobbers", b"noreturn"}
        keyword = state.expect(lex.TOKEN_KEYWORD)

        # fail if the keyword is not "clobbers" or "noreturn"
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
    token = state.expect(lex.TOKEN_IDENT)

    # expect opening round bracket
    state.expect(lex.TOKEN_ROUND_OPEN)

    # optional arguments
    if state.is_in(lex.TOKEN_HEX):
        arguments = parse_arguments(state)

    # expect closed round bracket
    state.expect(lex.TOKEN_ROUND_CLOSE)

    # expect a semicolon
    state.expect(lex.TOKEN_SEMICOLON)

    return ast.CallStatement(
        ref=state.span(token),
        name=state.extract(token),
        arguments=arguments,
    )


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
