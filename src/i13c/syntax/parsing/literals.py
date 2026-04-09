from i13c.syntax import tree
from i13c.syntax.lexing import Token
from i13c.syntax.parsing.core import InvalidHexLiteral, ParsingState


def extract_hex(state: ParsingState, token: Token) -> tree.literals.Hex:
    data = state.extract(token)

    if len(data) not in (4, 6, 10, 18):
        raise InvalidHexLiteral(token)

    return tree.literals.Hex(digits=bytes.fromhex(data[2:]))
