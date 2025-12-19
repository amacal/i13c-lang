from dataclasses import dataclass
from typing import List

CLASS_COMMA = b","
CLASS_NEWLINE = b"\n"
CLASS_WHITESPACE = b" "
CLASS_ZERO = b"0"
CLASS_LETTER = b"abcdefghijklmnopqrstuvwxyz"
CLASS_HEX = b"0123456789abcdef"

TOKEN_NEWLINE = 1
TOKEN_COMMA = 2
TOKEN_HEX = 3
TOKEN_IDENT = 4
TOKEN_EOF = 255

AFTER_HEX = CLASS_WHITESPACE + CLASS_COMMA + CLASS_NEWLINE
AFTER_IDENT = CLASS_WHITESPACE + CLASS_COMMA + CLASS_NEWLINE


class UnexpectedValue(Exception):
    def __init__(self, offset: int, expected: bytes) -> None:
        self.offset = offset
        self.expected = expected


class UnexpectedEndOfFile(Exception):
    def __init__(self, offset: int) -> None:
        self.offset = offset


class UnrecognizedToken(Exception):
    def __init__(
        self,
        offset: int,
    ) -> None:
        self.offset = offset


@dataclass(kw_only=True)
class Lexer:
    data: bytes
    offset: int

    def is_eof(self) -> bool:
        return self.offset >= len(self.data)

    def is_in(self, n: bytes) -> bool:
        return not self.is_eof() and self.data[self.offset] in n

    def extract(self, token: Token) -> bytes:
        return self.data[token.offset : token.offset + token.length]

    def advance(self, n: int) -> None:
        self.offset += n

    def expect(self, n: bytes) -> None:
        if self.is_eof():
            raise UnexpectedEndOfFile(self.offset)

        if not self.is_in(n):
            raise UnexpectedValue(self.offset, n)


@dataclass(kw_only=True)
class Token:
    code: int
    offset: int
    length: int

    @staticmethod
    def newline_token(offset: int) -> "Token":
        return Token(code=TOKEN_NEWLINE, offset=offset, length=1)

    @staticmethod
    def comma_token(offset: int) -> "Token":
        return Token(code=TOKEN_COMMA, offset=offset, length=1)

    @staticmethod
    def hex_token(offset: int, length: int) -> "Token":
        return Token(code=TOKEN_HEX, offset=offset, length=length)

    @staticmethod
    def ident_token(offset: int, length: int) -> "Token":
        return Token(code=TOKEN_IDENT, offset=offset, length=length)


def open_text(data: str) -> Lexer:
    return Lexer(data=data.encode("utf-8"), offset=0)


def tokenize(lexer: Lexer) -> List[Token]:
    tokens: List[Token] = []

    while not lexer.is_eof():
        skip_whitespace(lexer)

        if lexer.is_in(CLASS_NEWLINE):
            emit_newline(lexer, tokens)

        elif lexer.is_in(CLASS_COMMA):
            emit_comma(lexer, tokens)

        elif lexer.is_in(CLASS_ZERO):
            read_hex(lexer, tokens)

        elif lexer.is_in(CLASS_LETTER):
            read_ident(lexer, tokens)

        elif not lexer.is_eof():
            raise UnrecognizedToken(lexer.offset)

    return tokens


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

    # accept subsequent letters
    while not lexer.is_eof() and lexer.is_in(CLASS_LETTER):
        lexer.advance(1)  # consume letters

    # expect either EOF or valid character after ident
    if not lexer.is_eof() and not lexer.is_in(AFTER_IDENT):
        raise UnexpectedValue(lexer.offset, AFTER_IDENT)

    length = lexer.offset - start_offset
    tokens.append(Token.ident_token(offset=start_offset, length=length))


def emit_newline(lexer: Lexer, tokens: List[Token]) -> None:
    tokens.append(Token.newline_token(offset=lexer.offset))
    lexer.advance(1)  # consume newline


def emit_comma(lexer: Lexer, tokens: List[Token]) -> None:
    tokens.append(Token.comma_token(offset=lexer.offset))
    lexer.advance(1)  # consume comma
