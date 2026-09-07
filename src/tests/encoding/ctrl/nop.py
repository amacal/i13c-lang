from tests.encoding.core import encode

NOP = """
    | ----------- | -------- |
    | instruction | encoding |
    | ----------- | -------- |
    | nop         | 90       |
    | ----------- | -------- |
"""


def can_encode_nop():
    encode(NOP)
