from typing import Tuple

from i13c.syntax import tree
from i13c.syntax.lexing import Token, Tokens
from i13c.syntax.parsing.core import ParsingState
from i13c.syntax.parsing.literals import extract_hex


def parse_range(state: ParsingState) -> Tuple[tree.types.Range, Token]:
    # expect opening square bracket
    state.expect(Tokens.SQUARE_OPEN)
    lower = state.expect(Tokens.HEX)

    # expect range operator
    state.expect(Tokens.RANGE)
    upper = state.expect(Tokens.HEX)

    # expect closing square bracket
    end = state.expect(Tokens.SQUARE_CLOSE)

    # construct the range
    range = tree.types.Range(
        ref=state.between(lower, upper),
        lower=extract_hex(state, lower),
        upper=extract_hex(state, upper),
    )

    return range, end
