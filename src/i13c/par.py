from typing import List, Union
from dataclasses import dataclass
from i13c import lex, ast, src, res, diag


class UnexpectedTokenCode(Exception):
    def __init__(self, offset: int, expected: List[int], found: int) -> None:
        self.offset = offset
        self.expected = expected
        self.found = found


class UnexpectedEndOfTokens(Exception):
    def __init__(self, offset: int) -> None:
        self.offset = offset


@dataclass(kw_only=True)
class ParsingState:
    code: src.SourceCode
    tokens: List[lex.Token]
    position: int

    def is_eof(self) -> bool:
        return self.tokens[self.position].code == lex.TOKEN_EOF

    def is_in(self, *codes: int) -> bool:
        return self.tokens[self.position].code in codes

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
    instructions: List[ast.Instruction] = []
    diagnostics: List[diag.Diagnostic] = []

    try:
        while not state.is_eof():
            instructions.append(parse_instruction(state))

    except UnexpectedEndOfTokens as e:
        diagnostics.append(report_unexpected_end_of_tokens(e.offset))

    except UnexpectedTokenCode as e:
        diagnostics.append(report_unexpected_token(e.offset, e.expected, e.found))

    # any diagnostics stops further processing
    if diagnostics:
        return res.Err(diagnostics)

    return res.Ok(ast.Program(instructions=instructions))


def parse_instruction(state: ParsingState) -> ast.Instruction:
    operands = []
    token = state.expect(lex.TOKEN_MNEMONIC)

    # optional operands
    if state.is_in(lex.TOKEN_REG, lex.TOKEN_HEX):
        operands = parse_operands(state)

    # expect a semicolon
    state.expect(lex.TOKEN_SEMICOLON)

    # build instruction and token reference
    mnemonic = ast.Mnemonic(name=state.extract(token))
    ref = ast.Reference(offset=token.offset, length=token.length)

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
