from tests.encoding.core import encode, exhaust


def can_exhaust_loop():
    exhaust(LOOP_REL)


LOOP_REL = """
    | ------------------------------------------------- | ----------------------- |
    | instruction                                       | encoding                |
    | ------------------------------------------------- | ----------------------- |
    | .prev5: nop; nop; nop; nop; nop; loop @prev5      | 90 90 90 90 90 e2 f9    |
    | .prev1: nop; loop @prev1                          | 90 e2 fd                |
    | loop @next1; nop; .next1: nop                     | e2 01 90 90             |
    | loop @next5; nop; nop; nop; nop; nop; .next5: nop | e2 05 90 90 90 90 90 90 |
    | ------------------------------------------------- | ----------------------- |
"""


def can_encode_loop_rel():
    encode(LOOP_REL)
