from typing import List

from pytest import raises

from i13c.encoding import DuplicateLabelError, MissingLabelError, encode
from i13c.llvm.typing.flows import BlockId
from i13c.llvm.typing.instructions import Instruction
from i13c.llvm.typing.instructions.jump import Call, Jump, Label, Nop, Return, SysCall


def can_encode_instructions_nop_twice():
    flow: List[Instruction] = [
        Nop(),
        Nop(),
    ]

    bytecode = encode(flow)
    expected = bytes([0x90, 0x90])

    assert bytecode == expected

def can_encode_instructions_syscall():
    flow: List[Instruction] = [
        SysCall(),
    ]

    bytecode = encode(flow)
    expected = bytes([0x0F, 0x05])

    assert bytecode == expected


def can_encode_instructions_jump_forward():
    flow: List[Instruction] = [
        Jump(target=BlockId(value=1)),
        Nop(),
        Label(id=BlockId(value=1)),
    ]

    bytecode = encode(flow)
    expected = bytes([0xE9, 0x01, 0x00, 0x00, 0x00, 0x90])

    assert bytecode == expected


def can_encode_call_with_forward_relocation():
    flow: List[Instruction] = [
        Call(target=BlockId(value=1)),
        Return(),
        Label(id=BlockId(value=1)),
        Return(),
    ]

    bytecode = encode(flow)
    expected = bytes([0xE8, 0x01, 0x00, 0x00, 0x00, 0xC3, 0xC3])

    assert bytecode == expected


def can_reject_call_to_missing_label():
    flow: List[Instruction] = [Call(target=BlockId(value=9))]

    with raises(MissingLabelError) as error:
        encode(flow)

    assert isinstance(error.value, MissingLabelError)
    assert error.value.target > 0



def can_reject_duplicate_labels():
    flow: List[Instruction] = [
        Label(id=BlockId(value=1)),
        Return(),
        Label(id=BlockId(value=1)),
    ]

    with raises(DuplicateLabelError) as error:
        encode(flow)

    assert isinstance(error.value, DuplicateLabelError)
    assert error.value.target == 1
