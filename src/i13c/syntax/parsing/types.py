from i13c.syntax import tree
from i13c.syntax.lexing import Tokens
from i13c.syntax.parsing.core import ParsingState


def parse_range(state: ParsingState) -> tree.types.Range:
    # expect opening square bracket
    state.expect(Tokens.SQUARE_OPEN)
    lower = state.expect(Tokens.HEX)

    # expect range operator
    state.expect(Tokens.RANGE)
    upper = state.expect(Tokens.HEX)

    # expect closing square bracket
    state.expect(Tokens.SQUARE_CLOSE)

    return tree.types.Range(
        lower=tree.literals.Hex(digits=bytes.fromhex(state.extract(lower)[2:])),
        upper=tree.literals.Hex(digits=bytes.fromhex(state.extract(upper)[2:])),
    )
