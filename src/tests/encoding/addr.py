from typing import Optional

from i13c.llvm.typing.instructions import addr
from i13c.llvm.typing.instructions.core import Register, ScaleValue
from tests.encoding import encode_instruction, parse_address, samples


@samples(
    """
        | --- | ---- | ----- | ----- | ---------- | ----------------------- | --- | --- | ---- | ----- | ----- | ---------- | ----------------------- |
        | dst | base | scale | index | disp32     | encoding                | *** | dst | base | scale | index | disp32     | encoding                |
        | --- | ---- | ----- | ----- | ---------- | ----------------------- | --- | --- | ---- | ----- | ----- | ---------- | ----------------------- |
        | rax | rsi  | -     | -     | -          | 48 8d 06                | *** | eax | rsi  | -     | -     | -          | 8d 06                   |
        | rax | rsp  | -     | -     | -          | 48 8d 04 24             | *** | r8  | r12  | -     | -     | -          | 4d 8d 04 24             |
        | rax | rbp  | -     | -     | -          | 48 8d 45 00             | *** | r8  | r13  | -     | -     | -          | 4d 8d 45 00             |
        | rax | rdi  | -     | -     | 0x0000007f | 48 8d 47 7f             | *** | eax | rdi  | -     | -     | 0x00000080 | 8d 87 80 00 00 00       |
        | rax | rdi  | -     | -     | 0x00000080 | 48 8d 87 80 00 00 00    | *** | eax | rdi  | -     | -     | 0xffffff7f | 8d 87 7f ff ff ff       |
        | rax | -    | 1     | rdx   | -          | 48 8d 04 15 00 00 00 00 | *** | r8  | -    | 8     | r8    | -          | 4e 8d 04 c5 00 00 00 00 |
        | rax | rdi  | 4     | rbp   | -          | 48 8d 04 af             | *** | r8  | r12  | 2     | r10   | -          | 4f 8d 04 54             |
        | rax | rbp  | 8     | rbx   | -          | 48 8d 44 dd 00          | *** | r8  | r13  | 2     | r10   | -          | 4f 8d 44 55 00          |
        | rax | -    | -     | -     | 0x12345678 | 48 8d 04 25 78 56 34 12 | *** | r8  | -    | -     | -     | 0x12345678 | 4c 8d 04 25 78 56 34 12 |
        | rax | rip  | -     | -     | 0x00000000 | 48 8d 05 00 00 00 00    | *** | r9d | rip  | -     | -     | 0x12345678 | 44 8d 0d 78 56 34 12    |
        | rdx | rsi  | 1     | rsp   | -          | !! !! !! !! !! !! !! !! | *** | rax | rdi  | 1     | r12   | -          | 4a 8d 04 27             |
        | --- | ---- | ----- | ----- | ---------- | ----------------------- | --- | --- | ---- | ----- | ----- | ---------- | ----------------------- |
    """
)
def can_encode_lea(
    dst: str,
    base: Optional[str],
    scale: Optional[ScaleValue],
    index: Optional[str],
    disp32: Optional[int],
    encoding: Optional[bytes],
):

    encode_instruction(
        addr.LEA(
            dst=Register.auto(dst),
            src=parse_address(base, scale, index, disp32),
        ),
        encoding,
    )
