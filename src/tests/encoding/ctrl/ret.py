from tests.encoding.core import encode

RET = """
    | ----------- | -------- |
    | instruction | encoding |
    | ----------- | -------- |
    | ret         | c3       |
    | ----------- | -------- |
"""


def can_encode_ret():
    encode(RET)
