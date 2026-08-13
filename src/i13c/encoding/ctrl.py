
from i13c.encoding.core import LabelArtifact, RelocationArtifact
from i13c.llvm.typing.instructions.ctrl import Call, Jump, Label, Nop, Return, SysCall


def encode_syscall(
    instruction: SysCall, bytecode: bytearray
) -> LabelArtifact | RelocationArtifact | None:
    bytecode.extend([0x0F, 0x05])


def encode_return(
    instruction: Return, bytecode: bytearray
) -> LabelArtifact | RelocationArtifact | None:
    # C3 is simply RET
    bytecode.extend([0xC3])


def encode_label(
    instruction: Label, bytecode: bytearray
) -> LabelArtifact | RelocationArtifact | None:
    # record label position
    offset = len(bytecode)
    target = instruction.id.value

    # the label points at the current bytecode length
    return LabelArtifact(target=target, offset=offset)


def encode_call(
    instruction: Call, bytecode: bytearray
) -> LabelArtifact | RelocationArtifact | None:
    # emit E8 cd --- where cd is a signed 32-bit offset
    bytecode.extend([0xE8, 0x00, 0x00, 0x00, 0x00])

    # record relocation info
    offset = len(bytecode) - 4
    target = instruction.target.value

    # record relocation to be fixed up later
    return RelocationArtifact(target=target, offset=offset)


def encode_jump(
    instruction: Jump, bytecode: bytearray
) -> LabelArtifact | RelocationArtifact | None:
    # emit E9 cd --- where cd is a signed 32-bit offset
    bytecode.extend([0xE9, 0x00, 0x00, 0x00, 0x00])

    # record relocation info
    offset = len(bytecode) - 4
    target = instruction.target.value

    # record relocation to be fixed up later
    return RelocationArtifact(target=target, offset=offset)


def encode_nop(
    instruction: Nop, bytecode: bytearray
) -> LabelArtifact | RelocationArtifact | None:
    # 90 is simply NOP
    bytecode.extend([0x90])
