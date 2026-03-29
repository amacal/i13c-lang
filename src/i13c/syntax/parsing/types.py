from i13c.syntax import tree
from i13c.syntax.lexing import Tokens
from i13c.syntax.parsing.core import ParsingState


def parse_range(state: ParsingState) -> tree.Range:
    # expect opening square bracket
    state.expect(Tokens.SQUARE_OPEN)
    lower = state.expect(Tokens.HEX)

    # expect range operator
    state.expect(Tokens.RANGE)
    upper = state.expect(Tokens.HEX)

    # expect closing square bracket
    state.expect(Tokens.SQUARE_CLOSE)

    return tree.Range(
        lower=int(state.extract(lower), 16),
        upper=int(state.extract(upper), 16),
    )
