from i13c.semantic.typing.entities.asmlets import (
    AsmletOperandAddress,
    AsmletOperandImmediate,
    AsmletOperandRegister,
    AsmletOperandRelocation,
)
from tests.semantic.nodes.entities import prepare_entities


def can_do_nothing_without_any_snippet():
    entities = prepare_entities(
        """
            fn main() { }
        """
    )

    assert entities.asmlets is not None
    assert entities.asmlets.size() == 0


def can_do_nothing_without_any_callsite():
    entities = prepare_entities(
        """
            asm bar() { mov rax, rbx; }
            fn main() { }
        """
    )

    assert entities.asmlets is not None
    assert entities.asmlets.size() == 0


def can_substitute_a_snippet_without_any_parameters():
    entities = prepare_entities(
        """
            asm bar() { mov rax, rbx; }
            fn main() { bar(); }
        """
    )

    assert entities.asmlets is not None
    assert entities.asmlets.size() == 1
    _, asmlet = entities.asmlets.peak()

    assert entities.snippets.size() == 1
    id, _ = entities.snippets.peak()

    assert len(asmlet.keys) == 0
    assert len(asmlet.callsites) == 1

    assert asmlet.source == id
    assert len(asmlet.binding) == 0
    assert len(asmlet.parameters) == 0

    assert len(asmlet.instructions) == 1
    instr = asmlet.instructions[0]

    assert instr.mnemonic == b"mov"
    assert len(instr.operands) == 2

    assert instr.operands[0].symbol == "reg64"
    assert isinstance(instr.operands[0].target, AsmletOperandRegister)
    assert instr.operands[0].target.name == b"rax"

    assert instr.operands[1].symbol == "reg64"
    assert isinstance(instr.operands[1].target, AsmletOperandRegister)
    assert instr.operands[1].target.name == b"rbx"


def can_substitute_a_snippet_with_a_register_parameter():
    entities = prepare_entities(
        """
            asm bar(v@rcx: u8) { mov rax, @v; }
            fn main() { bar(0x01); }
        """
    )

    assert entities.asmlets is not None
    assert entities.asmlets.size() == 1
    _, asmlet = entities.asmlets.peak()

    assert len(asmlet.keys) == 0
    assert len(asmlet.callsites) == 1

    assert entities.snippets.size() == 1
    id, _ = entities.snippets.peak()

    assert asmlet.source == id
    assert len(asmlet.binding) == 1

    assert asmlet.binding[0].src == b"v"
    assert asmlet.binding[0].dst == b"rcx"
    assert asmlet.binding[0].mode == "register"

    assert len(asmlet.parameters) == 1
    assert asmlet.parameters[0].name == b"v"
    assert asmlet.parameters[0].type.name == b"u8"
    assert asmlet.parameters[0].type.width == 8

    assert len(asmlet.instructions) == 1
    instr = asmlet.instructions[0]

    assert instr.mnemonic == b"mov"
    assert len(instr.operands) == 2

    assert instr.operands[0].symbol == "reg64"
    assert isinstance(instr.operands[0].target, AsmletOperandRegister)
    assert instr.operands[0].target.name == b"rax"

    assert instr.operands[1].symbol == "reg64"
    assert isinstance(instr.operands[1].target, AsmletOperandRegister)
    assert instr.operands[1].target.name == b"rcx"


def can_substitute_a_snippet_with_a_base_register_parameter():
    entities = prepare_entities(
        """
            asm bar(v@rcx: u8) { mov rax, [@v]; }
            fn main() { bar(0x01); }
        """
    )

    assert entities.asmlets is not None
    assert entities.asmlets.size() == 1
    _, asmlet = entities.asmlets.peak()

    assert entities.snippets.size() == 1
    id, _ = entities.snippets.peak()

    assert len(asmlet.keys) == 0
    assert len(asmlet.callsites) == 1

    assert asmlet.source == id
    assert len(asmlet.binding) == 1

    assert asmlet.binding[0].src == b"v"
    assert asmlet.binding[0].dst == b"rcx"
    assert asmlet.binding[0].mode == "register"

    assert len(asmlet.parameters) == 1
    assert asmlet.parameters[0].name == b"v"
    assert asmlet.parameters[0].type.name == b"u8"
    assert asmlet.parameters[0].type.width == 8

    assert len(asmlet.instructions) == 1
    instr = asmlet.instructions[0]

    assert instr.mnemonic == b"mov"
    assert len(instr.operands) == 2

    assert instr.operands[0].symbol == "reg64"
    assert isinstance(instr.operands[0].target, AsmletOperandRegister)
    assert instr.operands[0].target.name == b"rax"

    assert instr.operands[1].symbol == "addr"
    assert isinstance(instr.operands[1].target, AsmletOperandAddress)
    assert instr.operands[1].target.base.name == b"rcx"
    assert instr.operands[1].target.displacement is None


def can_substitute_a_snippet_with_a_label_relocation_forward():
    entities = prepare_entities(
        """
            asm bar() { jmp @me; .me: nop; }
            fn main() { bar(); }
        """
    )

    assert entities.asmlets is not None
    assert entities.asmlets.size() == 1
    _, asmlet = entities.asmlets.peak()

    assert entities.snippets.size() == 1
    id, _ = entities.snippets.peak()

    assert len(asmlet.keys) == 0
    assert len(asmlet.callsites) == 1

    assert asmlet.source == id
    assert len(asmlet.binding) == 0
    assert len(asmlet.parameters) == 0

    assert len(asmlet.instructions) == 2
    instr = asmlet.instructions[0]

    assert instr.mnemonic == b"jmp"
    assert len(instr.operands) == 1

    assert instr.operands[0].symbol == "rel"
    assert isinstance(instr.operands[0].target, AsmletOperandRelocation)
    assert instr.operands[0].target.offset == 1


def can_substitute_a_snippet_with_a_label_relocation_backward():
    entities = prepare_entities(
        """
            asm bar() { .me: nop; jmp @me; }
            fn main() { bar(); }
        """
    )

    assert entities.asmlets is not None
    assert entities.asmlets.size() == 1
    _, asmlet = entities.asmlets.peak()

    assert entities.snippets.size() == 1
    id, _ = entities.snippets.peak()

    assert len(asmlet.keys) == 0
    assert len(asmlet.callsites) == 1

    assert asmlet.source == id
    assert len(asmlet.binding) == 0
    assert len(asmlet.parameters) == 0

    assert len(asmlet.instructions) == 2
    instr = asmlet.instructions[1]

    assert instr.mnemonic == b"jmp"
    assert len(instr.operands) == 1

    assert instr.operands[0].symbol == "rel"
    assert isinstance(instr.operands[0].target, AsmletOperandRelocation)
    assert instr.operands[0].target.offset == -1


def can_substitute_a_snippet_with_a_base_register_parameter_and_displacement():
    entities = prepare_entities(
        """
            asm bar(v@rcx: u8) { mov rax, [@v + 0x10]; }
            fn main() { bar(0x01); }
        """
    )

    assert entities.asmlets is not None
    assert entities.asmlets.size() == 1
    _, asmlet = entities.asmlets.peak()

    assert entities.snippets.size() == 1
    id, _ = entities.snippets.peak()

    assert len(asmlet.keys) == 0
    assert len(asmlet.callsites) == 1

    assert asmlet.source == id
    assert len(asmlet.binding) == 1

    assert asmlet.binding[0].src == b"v"
    assert asmlet.binding[0].dst == b"rcx"
    assert asmlet.binding[0].mode == "register"

    assert len(asmlet.parameters) == 1
    assert asmlet.parameters[0].name == b"v"
    assert asmlet.parameters[0].type.name == b"u8"
    assert asmlet.parameters[0].type.width == 8

    assert len(asmlet.instructions) == 1
    instr = asmlet.instructions[0]

    assert instr.mnemonic == b"mov"
    assert len(instr.operands) == 2

    assert instr.operands[0].symbol == "reg64"
    assert isinstance(instr.operands[0].target, AsmletOperandRegister)
    assert instr.operands[0].target.name == b"rax"

    assert instr.operands[1].symbol == "addr"
    assert isinstance(instr.operands[1].target, AsmletOperandAddress)
    assert instr.operands[1].target.base.name == b"rcx"

    assert instr.operands[1].target.displacement is not None
    assert instr.operands[1].target.displacement.width == 8
    assert instr.operands[1].target.displacement.data.hex() == "10"


def can_substitute_only_once_the_same_signatured_called_twice():
    entities = prepare_entities(
        """
            asm bar() { mov rax, rbx; }
            fn main() { bar(); bar(); }
        """
    )

    assert entities.asmlets is not None
    assert entities.asmlets.size() == 1

    _, asmlet = entities.asmlets.peak()
    assert len(asmlet.callsites) == 2


def can_substitute_only_once_the_same_signatured_called_twice_via_register():
    entities = prepare_entities(
        """
            asm bar(abc@rbx: u8) { mov rax, @abc; }
            fn main() { bar(0x01); bar(0x02); }
        """
    )

    assert entities.asmlets is not None
    assert entities.asmlets.size() == 1

    _, asmlet = entities.asmlets.peak()
    assert len(asmlet.callsites) == 2


def can_substitute_a_snippet_with_a_immediate_parameter():
    entities = prepare_entities(
        """
            asm bar(v@imm: u16) { mov rax, @v; }
            fn main() { bar(0x0001); }
        """
    )

    assert entities.asmlets is not None
    assert entities.asmlets.size() == 1
    _, asmlet = entities.asmlets.peak()

    assert entities.snippets.size() == 1
    id, _ = entities.snippets.peak()

    assert asmlet.source == id
    assert len(asmlet.binding) == 0
    assert len(asmlet.parameters) == 0
    assert len(asmlet.callsites) == 1

    assert len(asmlet.keys) == 1
    assert b"v" in asmlet.keys
    assert asmlet.keys[b"v"].width == 16
    assert asmlet.keys[b"v"].data.hex() == "0001"

    assert len(asmlet.instructions) == 1
    instr = asmlet.instructions[0]

    assert instr.mnemonic == b"mov"
    assert len(instr.operands) == 2

    assert instr.operands[0].symbol == "reg64"
    assert isinstance(instr.operands[0].target, AsmletOperandRegister)
    assert instr.operands[0].target.name == b"rax"

    assert instr.operands[1].symbol == "imm16"
    assert isinstance(instr.operands[1].target, AsmletOperandImmediate)

    assert instr.operands[1].target.value.width == 16
    assert instr.operands[1].target.value.data.hex() == "0001"


def can_substitute_a_snippet_with_a_immediate_parameter_once():
    entities = prepare_entities(
        """
            asm bar(v@imm: u16) { mov rax, @v; }
            fn main() { bar(0x0001); bar(0x0001); }
        """
    )

    assert entities.asmlets is not None
    assert entities.asmlets.size() == 1


def can_substitute_a_snippet_with_a_immediate_parameter_twice():
    entities = prepare_entities(
        """
            asm bar(v@imm: u16) { mov rax, @v; }
            fn main() { bar(0x0000); bar(0x0001); }
        """
    )

    assert entities.asmlets is not None
    assert entities.asmlets.size() == 2

    for idx, asmlet in enumerate(entities.asmlets.values()):
        assert entities.snippets.size() == 1
        id, _ = entities.snippets.peak()

        assert asmlet.source == id
        assert len(asmlet.binding) == 0
        assert len(asmlet.parameters) == 0
        assert len(asmlet.callsites) ==  1

        assert len(asmlet.keys) == 1
        assert b"v" in asmlet.keys
        assert asmlet.keys[b"v"].width == 16
        assert asmlet.keys[b"v"].data.hex() == f"000{idx}"

        assert len(asmlet.instructions) == 1
        instr = asmlet.instructions[0]

        assert instr.mnemonic == b"mov"
        assert len(instr.operands) == 2

        assert instr.operands[0].symbol == "reg64"
        assert isinstance(instr.operands[0].target, AsmletOperandRegister)
        assert instr.operands[0].target.name == b"rax"

        assert instr.operands[1].symbol == "imm16"
        assert isinstance(instr.operands[1].target, AsmletOperandImmediate)

        assert instr.operands[1].target.value.width == 16
        assert instr.operands[1].target.value.data.hex() == f"000{idx}"


# TODO: Support it
# def can_substitute_a_immediate_displacement():
#     entities = prepare_entities(
#         """
#             asm bar(v@imm: u8) { mov rax, [rcx + @v]; }
#             fn main() { bar(0x01); }
#         """
#     )

#     assert entities.asmlets is not None
#     assert entities.asmlets.size() == 1
#     _, asmlet = entities.asmlets.peak()

#     assert entities.snippets.size() == 1
#     id, _ = entities.snippets.peak()

#     assert asmlet.source == id
#     assert len(asmlet.binding) == 0
#     assert len(asmlet.parameters) == 0

#     assert len(asmlet.instructions) == 1
#     instr = asmlet.instructions[0]

#     assert instr.mnemonic == b"mov"
#     assert len(instr.operands) == 2

#     assert instr.operands[0].symbol == "reg64"
#     assert isinstance(instr.operands[0].target, AsmletOperandRegister)
#     assert instr.operands[0].target.name == b"rax"

#     assert instr.operands[1].symbol == "addr"
#     assert isinstance(instr.operands[1].target, AsmletOperandAddress)
#     assert instr.operands[1].target.base.name == b"rcx"

#     assert instr.operands[1].target.displacement is not None
#     assert instr.operands[1].target.displacement.width == 8
#     assert instr.operands[1].target.displacement.data.hex() == "01"
