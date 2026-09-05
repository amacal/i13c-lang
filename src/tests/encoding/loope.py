from tests.encoding.core import encode, exhaust


def can_exhaust_loope():
    exhaust(LOOPE_REL)


LOOPE_REL = """
    | ------------------------------------------------- | ----------------------- |
    | instruction                                       | encoding                |
    | ------------------------------------------------- | ----------------------- |
    | .prev5: nop; nop; nop; nop; nop; loope @prev5     | 90 90 90 90 90 e1 f9    |
    | .prev1: nop; loope @prev1                         | 90 e1 fd                |
    | loope @next1; nop; .next1: nop                    | e1 01 90 90             |
    | loope @next5; nop; nop; nop; nop; nop; .next5: nop | e1 05 90 90 90 90 90 90 |
    | ------------------------------------------------- | ----------------------- |
"""


def can_encode_loope_rel():
    encode(LOOPE_REL)
