from i13c.semantic.typing.analyses.asmlets import (
    AsmletOperandAddress,
    AsmletOperandImmediate,
    AsmletOperandRegister,
    AsmletOperandRelocation,
)
from tests.semantic.nodes.analyses import prepare_analyses


def can_do_nothing_without_any_snippet():
    _, analyses = prepare_analyses("""
        fn main() { }
    """)

    assert analyses.asmlets is not None
    assert analyses.asmlets.size() == 0


def can_do_nothing_without_any_callsite():
    _, analyses = prepare_analyses("""
        asm bar() { mov rax, rbx; }
        fn main() { }
    """)

    assert analyses.asmlets is not None
    assert analyses.asmlets.size() == 0


def can_substitute_a_snippet_without_any_parameters():
    entities, analyses = prepare_analyses("""
        asm bar() { mov rax, rbx; }
        fn main() { bar(); }
    """)

    assert analyses.asmlets is not None
    assert analyses.asmlets.size() == 1
    _, asmlet = analyses.asmlets.peak()

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
    entities, analyses = prepare_analyses("""
        asm bar(v@rcx: u8) { mov rax, @v; }
        fn main() { bar(0x01); }
    """)

    assert analyses.asmlets is not None
    assert analyses.asmlets.size() == 1
    _, asmlet = analyses.asmlets.peak()

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
    entities, analyses = prepare_analyses("""
        asm bar(v@rcx: u8) { mov rax, [@v]; }
        fn main() { bar(0x01); }
    """)

    assert analyses.asmlets is not None
    assert analyses.asmlets.size() == 1
    _, asmlet = analyses.asmlets.peak()

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
    entities, analyses = prepare_analyses("""
        asm bar() { jmp @me; .me: nop; }
        fn main() { bar(); }
    """)

    assert analyses.asmlets is not None
    assert analyses.asmlets.size() == 1
    _, asmlet = analyses.asmlets.peak()

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
    entities, analyses = prepare_analyses("""
        asm bar() { .me: nop; jmp @me; }
        fn main() { bar(); }
    """)

    assert analyses.asmlets is not None
    assert analyses.asmlets.size() == 1
    _, asmlet = analyses.asmlets.peak()

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
    entities, analyses = prepare_analyses("""
        asm bar(v@rcx: u8) { mov rax, [@v + 0x10]; }
        fn main() { bar(0x01); }
    """)

    assert analyses.asmlets is not None
    assert analyses.asmlets.size() == 1
    _, asmlet = analyses.asmlets.peak()

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
    _, analyses = prepare_analyses("""
        asm bar() { mov rax, rbx; }
        fn main() { bar(); bar(); }
    """)

    assert analyses.asmlets is not None
    assert analyses.asmlets.size() == 1

    _, asmlet = analyses.asmlets.peak()
    assert len(asmlet.callsites) == 2


def can_substitute_only_once_the_same_signatured_called_twice_via_register():
    _, analyses = prepare_analyses("""
        asm bar(abc@rbx: u8) { mov rax, @abc; }
        fn main() { bar(0x01); bar(0x02); }
    """)

    assert analyses.asmlets is not None
    assert analyses.asmlets.size() == 1

    _, asmlet = analyses.asmlets.peak()
    assert len(asmlet.callsites) == 2


def can_substitute_a_snippet_with_a_immediate_parameter():
    entities, analyses = prepare_analyses("""
        asm bar(v@imm: u16) { mov rax, @v; }
        fn main() { bar(0x0001); }
    """)

    assert analyses.asmlets is not None
    assert analyses.asmlets.size() == 1
    _, asmlet = analyses.asmlets.peak()

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
    _, analyses = prepare_analyses("""
        asm bar(v@imm: u16) { mov rax, @v; }
        fn main() { bar(0x0001); bar(0x0001); }
    """)

    assert analyses.asmlets is not None
    assert analyses.asmlets.size() == 1


def can_substitute_a_snippet_with_a_immediate_parameter_twice():
    entities, analyses = prepare_analyses("""
        asm bar(v@imm: u16) { mov rax, @v; }
        fn main() { bar(0x0000); bar(0x0001); }
    """)

    assert analyses.asmlets is not None
    assert analyses.asmlets.size() == 2

    for idx, asmlet in enumerate(analyses.asmlets.values()):
        assert entities.snippets.size() == 1
        id, _ = entities.snippets.peak()

        assert asmlet.source == id
        assert len(asmlet.binding) == 0
        assert len(asmlet.parameters) == 0
        assert len(asmlet.callsites) == 1

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


def can_substitute_a_snippet_with_a_direct_immediate_operand():
    _, analyses = prepare_analyses("""
        asm bar() { mov rax, 0x0001; }
        fn main() { bar(); }
    """)

    assert analyses.asmlets is not None
    assert analyses.asmlets.size() == 1

    _, asmlet = analyses.asmlets.peak()
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


def can_substitute_a_snippet_with_two_immediate_parameters():
    _, analyses = prepare_analyses("""
        asm bar(x@imm: u8, y@imm: u16) { mov rax, @x; mov rax, @y; }
        fn main() { bar(0x01, 0x0002); }
    """)

    assert analyses.asmlets is not None
    assert analyses.asmlets.size() == 1

    _, asmlet = analyses.asmlets.peak()

    assert len(asmlet.binding) == 0
    assert len(asmlet.parameters) == 0
    assert len(asmlet.keys) == 2

    assert asmlet.keys[b"x"].width == 8
    assert asmlet.keys[b"x"].data.hex() == "01"

    assert asmlet.keys[b"y"].width == 16
    assert asmlet.keys[b"y"].data.hex() == "0002"
