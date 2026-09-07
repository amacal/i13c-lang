from tests.encoding.core import encode, exhaust


def can_exhaust_loopne():
    exhaust(LOOPNE_REL)


LOOPNE_REL = """
    | -------------------------------------------------- | ----------------------- |
    | instruction                                        | encoding                |
    | -------------------------------------------------- | ----------------------- |
    | .prev5: nop; nop; nop; nop; nop; loopne @prev5     | 90 90 90 90 90 e0 f9    |
    | .prev1: nop; loopne @prev1                         | 90 e0 fd                |
    | loopne @next1; nop; .next1: nop                    | e0 01 90 90             |
    | loopne @next5; nop; nop; nop; nop; nop; .next5: nop | e0 05 90 90 90 90 90 90 |
    | -------------------------------------------------- | ----------------------- |
"""


def can_encode_loopne_rel():
    encode(LOOPNE_REL)
