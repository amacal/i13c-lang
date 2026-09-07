from tests.encoding.core import encode

SYSCALL = """
    | ----------- | -------- |
    | instruction | encoding |
    | ----------- | -------- |
    | syscall     | 0f 05    |
    | ----------- | -------- |
"""


def can_encode_syscall():
    encode(SYSCALL)
