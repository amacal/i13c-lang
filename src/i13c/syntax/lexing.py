from dataclasses import dataclass
from typing import Dict, List

from i13c.core import result
from i13c.core.diagnostics import Diagnostic
from i13c.syntax.source import SourceCode, Span

# - tabulators and other whitespace characters are
#   on purpose excluded to enforce only spaces and newlines
# - carriage return is not allowed to avoid Windows (CRLF) line endings
# - hex digits are lowercase only to simplify the lexer
#
# it is a language design decision not a limitation of the lexer

CLASS_AT = b"@"
CLASS_DOT = b"."
CLASS_COMMA = b","
CLASS_COLON = b":"
CLASS_PLUS = b"+"
CLASS_MINUS = b"-"
CLASS_SEMICOLON = b";"
CLASS_WHITESPACE = b" \n"
CLASS_UNDERSCORE = b"_"
CLASS_ZERO = b"0"
CLASS_EQUALS = b"="
CLASS_ROUND_OPEN = b"("
CLASS_ROUND_CLOSE = b")"
CLASS_CURLY_OPEN = b"{"
CLASS_CURLY_CLOSE = b"}"
CLASS_SQUARE_OPEN = b"["
CLASS_SQUARE_CLOSE = b"]"
CLASS_LETTER = b"abcdefghijklmnopqrstuvwxyz"
CLASS_ALPHANUM = b"abcdefghijklmnopqrstuvwxyz0123456789"
CLASS_HEX = b"0123456789abcdef"


class Tokens:
    SEMICOLON = 1
    COMMA = 2
    HEX = 3
    IDENT = 4
    RANGE = 6
    KEYWORD = 7
    ROUND_OPEN = 8
    ROUND_CLOSE = 9
    CURLY_OPEN = 10
    CURLY_CLOSE = 11
    AT = 12
    COLON = 13
    SQUARE_OPEN = 15
    SQUARE_CLOSE = 16
    EQUALS = 17
    PLUS = 18
    MINUS = 19
    DOT = 20
    EOF = 255


# fmt: off
SEPARATORS = (
    CLASS_WHITESPACE + CLASS_COMMA + CLASS_SEMICOLON +
    CLASS_ROUND_OPEN + CLASS_ROUND_CLOSE +
    CLASS_CURLY_OPEN + CLASS_CURLY_CLOSE +
    CLASS_SQUARE_OPEN + CLASS_SQUARE_CLOSE +
    CLASS_AT + CLASS_COLON + CLASS_DOT + CLASS_EQUALS +
    CLASS_PLUS + CLASS_MINUS
)

SET_KEYWORDS = {
    b"asm", b"clobbers", b"noreturn", b"fn", b"imm", b"val",
}

TOKEN_NAMES: Dict[int, str] = {
    Tokens.SEMICOLON: "semicolon",
    Tokens.COMMA: "comma",
    Tokens.HEX: "hex",
    Tokens.IDENT: "identifier",
    Tokens.RANGE: "range",
    Tokens.KEYWORD: "keyword",
    Tokens.ROUND_OPEN: "round-open",
    Tokens.ROUND_CLOSE: "round-close",
    Tokens.CURLY_OPEN: "curly-open",
    Tokens.CURLY_CLOSE: "curly-close",
    Tokens.AT: "at",
    Tokens.DOT: "dot",
    Tokens.COLON: "colon",
    Tokens.EQUALS: "equals",
    Tokens.SQUARE_OPEN: "square-open",
    Tokens.SQUARE_CLOSE: "square-close",
    Tokens.EOF: "end-of-file",
}
# fmt: on


class TooLargeHex(Exception):
    def __init__(self, offset: int, length: int) -> None:
        self.offset = offset
        self.length = length


class UnexpectedValue(Exception):
    def __init__(self, offset: int, expected: bytes) -> None:
        self.offset = offset
        self.expected = expected


class UnexpectedEndOfFile(Exception):
    def __init__(self, offset: int) -> None:
        self.offset = offset


@dataclass(kw_only=True)
class Lexer:
    code: SourceCode
    offset: int

    def is_eof(self) -> bool:
        return self.code.is_eof(self.offset)

    def is_in(self, *n: bytes) -> bool:
        if self.is_eof():
            return False

        return any(self.code.at(self.offset) in chars for chars in n)

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
    def semicolon_token(offset: int) -> Token:
        return Token(code=Tokens.SEMICOLON, offset=offset, length=1)

    @staticmethod
    def comma_token(offset: int) -> Token:
        return Token(code=Tokens.COMMA, offset=offset, length=1)

    @staticmethod
    def eof_token(offset: int) -> Token:
        return Token(code=Tokens.EOF, offset=offset, length=0)

    @staticmethod
    def hex_token(offset: int, length: int) -> Token:
        return Token(code=Tokens.HEX, offset=offset, length=length)

    @staticmethod
    def ident_token(offset: int, length: int) -> Token:
        return Token(code=Tokens.IDENT, offset=offset, length=length)

    @staticmethod
    def dot_token(offset: int) -> Token:
        return Token(code=Tokens.DOT, offset=offset, length=1)

    @staticmethod
    def range_token(offset: int, length: int) -> Token:
        return Token(code=Tokens.RANGE, offset=offset, length=length)

    @staticmethod
    def keyword_token(offset: int, length: int) -> Token:
        return Token(code=Tokens.KEYWORD, offset=offset, length=length)

    @staticmethod
    def round_open_token(offset: int) -> Token:
        return Token(code=Tokens.ROUND_OPEN, offset=offset, length=1)

    @staticmethod
    def round_close_token(offset: int) -> Token:
        return Token(code=Tokens.ROUND_CLOSE, offset=offset, length=1)

    @staticmethod
    def curly_open_token(offset: int) -> Token:
        return Token(code=Tokens.CURLY_OPEN, offset=offset, length=1)

    @staticmethod
    def curly_close_token(offset: int) -> Token:
        return Token(code=Tokens.CURLY_CLOSE, offset=offset, length=1)

    @staticmethod
    def square_open_token(offset: int) -> Token:
        return Token(code=Tokens.SQUARE_OPEN, offset=offset, length=1)

    @staticmethod
    def square_close_token(offset: int) -> Token:
        return Token(code=Tokens.SQUARE_CLOSE, offset=offset, length=1)

    @staticmethod
    def at_token(offset: int) -> Token:
        return Token(code=Tokens.AT, offset=offset, length=1)

    @staticmethod
    def colon_token(offset: int) -> Token:
        return Token(code=Tokens.COLON, offset=offset, length=1)

    @staticmethod
    def equals_token(offset: int) -> Token:
        return Token(code=Tokens.EQUALS, offset=offset, length=1)


def tokenize(code: SourceCode) -> result.Result[List[Token], List[Diagnostic]]:
    tokens: List[Token] = []
    diagnostics: List[Diagnostic] = []
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

            elif lexer.is_in(CLASS_SQUARE_OPEN):
                emit_square_open(lexer, tokens)

            elif lexer.is_in(CLASS_SQUARE_CLOSE):
                emit_square_close(lexer, tokens)

            elif lexer.is_in(CLASS_AT):
                emit_at(lexer, tokens)

            elif lexer.is_in(CLASS_COLON):
                emit_colon(lexer, tokens)

            elif lexer.is_in(CLASS_EQUALS):
                emit_equals(lexer, tokens)

            elif lexer.is_in(CLASS_PLUS):
                emit_plus(lexer, tokens)

            elif lexer.is_in(CLASS_MINUS):
                emit_minus(lexer, tokens)

            elif lexer.is_in(CLASS_DOT):
                read_dot(lexer, tokens)

            elif lexer.is_in(CLASS_ZERO):
                read_hex(lexer, tokens)

            elif lexer.is_in(CLASS_LETTER):
                read_ident(lexer, tokens)

            # unrecognized token
            elif not lexer.is_eof():
                diagnostics.append(report_e1000_unrecognized_token(lexer.offset))
                break

    except TooLargeHex as e:
        diagnostics.append(report_e1003_too_large_hex(e.offset, e.length))

    except UnexpectedEndOfFile as e:
        diagnostics.append(report_e1001_unexpected_end_of_file(e.offset))

    except UnexpectedValue as e:
        diagnostics.append(report_e1002_unexpected_value(e.offset, e.expected))

    # any diagnostics stops further processing
    if diagnostics:
        return result.Err(diagnostics)

    # append last EOF token
    tokens.append(Token.eof_token(offset=lexer.offset))

    return result.Ok(tokens)


def skip_whitespace(lexer: Lexer) -> None:
    while not lexer.is_eof() and lexer.is_in(CLASS_WHITESPACE):
        lexer.advance(1)


def read_dot(lexer: Lexer, tokens: List[Token]) -> None:
    start_offset = lexer.offset
    lexer.advance(1)  # consume the '.'

    # perhaps it's a single dot token
    if not lexer.is_in(CLASS_DOT):
        token = Token.dot_token(offset=start_offset)

    # handle range token with two dots
    else:
        lexer.advance(1)  # consume the second '.'
        token = Token.range_token(offset=start_offset, length=2)

    # success
    tokens.append(token)


def read_hex(lexer: Lexer, tokens: List[Token]) -> None:
    start_offset = lexer.offset
    lexer.advance(1)  # consume the '0'

    lexer.expect(b"x")
    lexer.advance(1)  # consume the 'x'

    # be explicit about EOF
    if lexer.is_eof():
        raise UnexpectedEndOfFile(lexer.offset)

    # accept subsequent hex digits
    while not lexer.is_eof() and lexer.is_in(CLASS_HEX):
        lexer.advance(1)  # consume hex digits

        # literals larger than 16 hex digits are rejected, even with leading zeros
        # it is design decision to limit hex literals to 64 bits to simplify the lexer
        if lexer.offset - start_offset > 18:
            raise TooLargeHex(start_offset, lexer.offset - start_offset)

    # 0x alone is not valid hex
    if lexer.offset - start_offset <= 2:
        raise UnexpectedValue(lexer.offset, CLASS_HEX)

    # expect either EOF or valid character after hex
    if not lexer.is_eof() and not lexer.is_in(SEPARATORS):
        raise UnexpectedValue(lexer.offset, SEPARATORS)

    length = lexer.offset - start_offset
    tokens.append(Token.hex_token(offset=start_offset, length=length))


def read_ident(lexer: Lexer, tokens: List[Token]) -> None:
    start_offset = lexer.offset
    lexer.advance(1)  # consume first letter

    # accept subsequent letters or digits
    while not lexer.is_eof() and lexer.is_in(CLASS_ALPHANUM + CLASS_UNDERSCORE):
        lexer.advance(1)  # consume letters and digits

    # expect either EOF or valid character after ident
    if not lexer.is_eof() and not lexer.is_in(SEPARATORS):
        raise UnexpectedValue(lexer.offset, SEPARATORS)

    length = lexer.offset - start_offset
    token = Token.ident_token(offset=start_offset, length=length)

    # perhaps it's a keyword
    if lexer.extract(token) in SET_KEYWORDS:
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


def emit_square_open(lexer: Lexer, tokens: List[Token]) -> None:
    tokens.append(Token.square_open_token(offset=lexer.offset))
    lexer.advance(1)  # consume '['


def emit_square_close(lexer: Lexer, tokens: List[Token]) -> None:
    tokens.append(Token.square_close_token(offset=lexer.offset))
    lexer.advance(1)  # consume ']'


def emit_colon(lexer: Lexer, tokens: List[Token]) -> None:
    tokens.append(Token.colon_token(offset=lexer.offset))
    lexer.advance(1)  # consume ':'


def emit_at(lexer: Lexer, tokens: List[Token]) -> None:
    tokens.append(Token.at_token(offset=lexer.offset))
    lexer.advance(1)  # consume '@'


def emit_equals(lexer: Lexer, tokens: List[Token]) -> None:
    tokens.append(Token.equals_token(offset=lexer.offset))
    lexer.advance(1)  # consume '='


def emit_plus(lexer: Lexer, tokens: List[Token]) -> None:
    tokens.append(Token(code=Tokens.PLUS, offset=lexer.offset, length=1))
    lexer.advance(1)  # consume '+'


def emit_minus(lexer: Lexer, tokens: List[Token]) -> None:
    tokens.append(Token(code=Tokens.MINUS, offset=lexer.offset, length=1))
    lexer.advance(1)  # consume '-'


def report_e1000_unrecognized_token(offset: int) -> Diagnostic:
    return Diagnostic(
        code="E1000",
        ref=Span(offset=offset, length=1),
        message="Unrecognized token",
    )


def report_e1001_unexpected_end_of_file(offset: int) -> Diagnostic:
    return Diagnostic(
        code="E1001",
        ref=Span(offset=offset, length=1),
        message="Unexpected end of file",
    )


def report_e1002_unexpected_value(offset: int, expected: bytes) -> Diagnostic:
    characters = [repr(chr(character)) for character in sorted(expected)]

    return Diagnostic(
        code="E1002",
        ref=Span(offset=offset, length=1),
        message=f"Unexpected value at offset {offset}, expected one of: {characters}",
    )


def report_e1003_too_large_hex(offset: int, length: int) -> Diagnostic:
    return Diagnostic(
        code="E1003",
        ref=Span(offset=offset, length=length),
        message=f"Hexadecimal literal too large at offset {offset}",
    )
