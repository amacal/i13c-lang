from dataclasses import dataclass
from typing import List, Set, Union

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


class InvalidHexLiteral(Exception):
    def __init__(self, token: LexingToken) -> None:
        self.token = token



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
