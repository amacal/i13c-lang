from dataclasses import dataclass
from typing import List
from i13c import src, res, diag

CLASS_COMMA = b","
CLASS_SEMICOLON = b";"
CLASS_WHITESPACE = b" \n"
CLASS_ZERO = b"0"
CLASS_ROUND_OPEN = b"("
CLASS_ROUND_CLOSE = b")"
CLASS_CURLY_OPEN = b"{"
CLASS_CURLY_CLOSE = b"}"
CLASS_LETTER = b"abcdefghijklmnopqrstuvwxyz"
CLASS_ALPHANUM = b"abcdefghijklmnopqrstuvwxyz0123456789"
CLASS_HEX = b"0123456789abcdef"

TOKEN_SEMICOLON = 1
TOKEN_COMMA = 2
TOKEN_HEX = 3
TOKEN_IDENT = 4
TOKEN_REG = 5
TOKEN_MNEMONIC = 6
TOKEN_KEYWORD = 7
TOKEN_ROUND_OPEN = 8
TOKEN_ROUND_CLOSE = 9
TOKEN_CURLY_OPEN = 10
TOKEN_CURLY_CLOSE = 11
TOKEN_EOF = 255

AFTER_HEX = CLASS_WHITESPACE + CLASS_COMMA + CLASS_SEMICOLON
AFTER_IDENT = CLASS_WHITESPACE + CLASS_COMMA + CLASS_SEMICOLON

# fmt: off
SET_REGS = {
    b"rax", b"rbx", b"rcx", b"rdx", b"rsi", b"rdi", b"rsp", b"rbp",
    b"r8", b"r9", b"r10", b"r11", b"r12", b"r13", b"r14", b"r15",
}

SET_MNEMONICS = {
    b"mov", b"syscall",
}

SET_KEYWORDS = {
    b"asm",
}
# fmt: on


class UnexpectedValue(Exception):
    def __init__(self, offset: int, expected: bytes) -> None:
        self.offset = offset
        self.expected = expected


class UnexpectedEndOfFile(Exception):
    def __init__(self, offset: int) -> None:
        self.offset = offset


@dataclass(kw_only=True)
class Lexer:
    code: src.SourceCode
    offset: int

    def is_eof(self) -> bool:
        return self.code.is_eof(self.offset)

    def is_in(self, n: bytes) -> bool:
        return not self.is_eof() and self.code.at(self.offset) in n

    def extract(self, token: Token) -> bytes:
        return self.code.extract(token)

    def advance(self, n: int) -> None:
        self.offset += n

    def expect(self, n: bytes) -> None:
        if self.is_eof():
            raise UnexpectedEndOfFile(self.offset)

        if not self.is_in(n):
            raise UnexpectedValue(self.offset, n)


@dataclass(kw_only=True)
class Reference:
    offset: int
    length: int


@dataclass(kw_only=True)
class Token:
    code: int
    offset: int
    length: int

    @staticmethod
    def semicolon_token(offset: int) -> "Token":
        return Token(code=TOKEN_SEMICOLON, offset=offset, length=1)

    @staticmethod
    def comma_token(offset: int) -> "Token":
        return Token(code=TOKEN_COMMA, offset=offset, length=1)

    @staticmethod
    def eof_token(offset: int) -> "Token":
        return Token(code=TOKEN_EOF, offset=offset, length=0)

    @staticmethod
    def hex_token(offset: int, length: int) -> "Token":
        return Token(code=TOKEN_HEX, offset=offset, length=length)

    @staticmethod
    def ident_token(offset: int, length: int) -> "Token":
        return Token(code=TOKEN_IDENT, offset=offset, length=length)

    @staticmethod
    def reg_token(offset: int, length: int) -> "Token":
        return Token(code=TOKEN_REG, offset=offset, length=length)

    @staticmethod
    def mnemonic_token(offset: int, length: int) -> "Token":
        return Token(code=TOKEN_MNEMONIC, offset=offset, length=length)

    @staticmethod
    def keyword_token(offset: int, length: int) -> "Token":
        return Token(code=TOKEN_KEYWORD, offset=offset, length=length)

    @staticmethod
    def round_open_token(offset: int) -> "Token":
        return Token(code=TOKEN_ROUND_OPEN, offset=offset, length=1)

    @staticmethod
    def round_close_token(offset: int) -> "Token":
        return Token(code=TOKEN_ROUND_CLOSE, offset=offset, length=1)

    @staticmethod
    def curly_open_token(offset: int) -> "Token":
        return Token(code=TOKEN_CURLY_OPEN, offset=offset, length=1)

    @staticmethod
    def curly_close_token(offset: int) -> "Token":
        return Token(code=TOKEN_CURLY_CLOSE, offset=offset, length=1)


def tokenize(code: src.SourceCode) -> res.Result[List[Token], List[diag.Diagnostic]]:
    tokens: List[Token] = []
    diagnostics: List[diag.Diagnostic] = []
    lexer = Lexer(code=code, offset=0)

    try:
        while not lexer.is_eof():
            skip_whitespace(lexer)

            if lexer.is_in(CLASS_SEMICOLON):
                emit_semicolon(lexer, tokens)

            elif lexer.is_in(CLASS_COMMA):
                emit_comma(lexer, tokens)

            elif lexer.is_in(CLASS_ROUND_OPEN):
                emit_round_open(lexer, tokens)

            elif lexer.is_in(CLASS_ROUND_CLOSE):
                emit_round_close(lexer, tokens)

            elif lexer.is_in(CLASS_CURLY_OPEN):
                emit_curly_open(lexer, tokens)

            elif lexer.is_in(CLASS_CURLY_CLOSE):
                emit_curly_close(lexer, tokens)

            elif lexer.is_in(CLASS_ZERO):
                read_hex(lexer, tokens)

            elif lexer.is_in(CLASS_LETTER):
                read_ident(lexer, tokens)

            # unrecognized token
            elif not lexer.is_eof():
                diagnostics.append(report_unrecognized_token(lexer.offset))
                break

    except UnexpectedEndOfFile as e:
        diagnostics.append(report_unexpected_end_of_file(e.offset))

    except UnexpectedValue as e:
        diagnostics.append(report_unexpected_value(e.offset, e.expected))

    # any diagnostics stops further processing
    if diagnostics:
        return res.Err(diagnostics)

    # append last EOF token
    tokens.append(Token.eof_token(offset=lexer.offset))

    return res.Ok(tokens)


def skip_whitespace(lexer: Lexer) -> None:
    while not lexer.is_eof() and lexer.is_in(CLASS_WHITESPACE):
        lexer.advance(1)


def read_hex(lexer: Lexer, tokens: List[Token]) -> None:
    start_offset = lexer.offset
    lexer.advance(1)  # consume the '0'

    lexer.expect(b"x")
    lexer.advance(1)  # consume the 'x'

    # accept subsequent hex digits
    while not lexer.is_eof() and lexer.is_in(CLASS_HEX):
        lexer.advance(1)  # consume hex digits

    # 0x alone is not valid hex
    if lexer.offset - start_offset <= 2:
        raise UnexpectedValue(lexer.offset, CLASS_HEX)

    # expect either EOF or valid character after hex
    if not lexer.is_eof() and not lexer.is_in(AFTER_HEX):
        raise UnexpectedValue(lexer.offset, AFTER_HEX)

    length = lexer.offset - start_offset
    tokens.append(Token.hex_token(offset=start_offset, length=length))


def read_ident(lexer: Lexer, tokens: List[Token]) -> None:
    start_offset = lexer.offset
    lexer.advance(1)  # consume first letter

    # accept subsequent letters or digits
    while not lexer.is_eof() and lexer.is_in(CLASS_ALPHANUM):
        lexer.advance(1)  # consume letters and digits

    # expect either EOF or valid character after ident
    if not lexer.is_eof() and not lexer.is_in(AFTER_IDENT):
        raise UnexpectedValue(lexer.offset, AFTER_IDENT)

    length = lexer.offset - start_offset
    token = Token.ident_token(offset=start_offset, length=length)

    # perhaps it's a register
    if lexer.extract(token) in SET_REGS:
        token = Token.reg_token(offset=start_offset, length=length)

    # perhaps it's a mnemonic
    elif lexer.extract(token) in SET_MNEMONICS:
        token = Token.mnemonic_token(offset=start_offset, length=length)

    # perhaps it's a keyword
    elif lexer.extract(token) in SET_KEYWORDS:
        token = Token.keyword_token(offset=start_offset, length=length)

    tokens.append(token)


def emit_semicolon(lexer: Lexer, tokens: List[Token]) -> None:
    tokens.append(Token.semicolon_token(offset=lexer.offset))
    lexer.advance(1)  # consume semicolon


def emit_comma(lexer: Lexer, tokens: List[Token]) -> None:
    tokens.append(Token.comma_token(offset=lexer.offset))
    lexer.advance(1)  # consume comma


def emit_round_open(lexer: Lexer, tokens: List[Token]) -> None:
    tokens.append(Token.round_open_token(offset=lexer.offset))
    lexer.advance(1)  # consume '('


def emit_round_close(lexer: Lexer, tokens: List[Token]) -> None:
    tokens.append(Token.round_close_token(offset=lexer.offset))
    lexer.advance(1)  # consume ')'


def emit_curly_open(lexer: Lexer, tokens: List[Token]) -> None:
    tokens.append(Token.curly_open_token(offset=lexer.offset))
    lexer.advance(1)  # consume '{'


def emit_curly_close(lexer: Lexer, tokens: List[Token]) -> None:
    tokens.append(Token.curly_close_token(offset=lexer.offset))
    lexer.advance(1)  # consume '}'


def report_unrecognized_token(offset: int) -> diag.Diagnostic:
    return diag.Diagnostic(
        offset=offset,
        code="L001",
        message="Unrecognized token",
    )


def report_unexpected_end_of_file(offset: int) -> diag.Diagnostic:
    return diag.Diagnostic(
        offset=offset,
        code="L002",
        message="Unexpected end of file",
    )


def report_unexpected_value(offset: int, expected: bytes) -> diag.Diagnostic:
    return diag.Diagnostic(
        offset=offset,
        code="L003",
        message=f"Unexpected value at offset {offset}, expected one of: {list(expected)}",
    )
