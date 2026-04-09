from i13c.core.result import Err, Ok
from i13c.syntax import tree
from i13c.syntax.lexing import tokenize
from i13c.syntax.parsing import parse
from i13c.syntax.source import open_text
from tests.syntax.parsing import parse_snippet


def can_parse_snippets_with_single_arg():
    snippet = parse_snippet("asm exit(code@rdi: u32) { syscall; }")

    assert snippet.name == b"exit"
    assert snippet.noreturn is False
    assert len(snippet.instructions) == 1

    instruction = snippet.instructions[0]
    assert instruction.mnemonic.name == b"syscall"
    assert len(instruction.operands) == 0

    slots = snippet.slots
    assert len(slots) == 1

    slot = slots[0]
    assert slot.name == b"code"
    assert slot.type.name == b"u32"

    assert isinstance(slot.bind, tree.snippet.Binding)
    assert slot.bind.name == b"rdi"


def can_parse_snippets_with_multiple_args():
    snippet = parse_snippet("asm exit(code@rdi: u32, id@rax: u16) { syscall; }")

    assert snippet.name == b"exit"
    assert snippet.noreturn is False
    assert len(snippet.instructions) == 1

    instruction = snippet.instructions[0]
    assert instruction.mnemonic.name == b"syscall"
    assert len(instruction.operands) == 0

    slots = snippet.slots
    assert len(slots) == 2

    slot1 = slots[0]
    assert slot1.name == b"code"
    assert slot1.type.name == b"u32"

    assert isinstance(slot1.bind, tree.snippet.Binding)
    assert slot1.bind.name == b"rdi"

    slot2 = slots[1]
    assert slot2.name == b"id"
    assert slot2.type.name == b"u16"

    assert isinstance(slot2.bind, tree.snippet.Binding)
    assert slot2.bind.name == b"rax"


def can_parse_snippets_with_bind_to_immediate():
    snippet = parse_snippet("asm exit(code@imm: u32) { }")

    assert snippet.name == b"exit"
    assert snippet.noreturn is False
    assert len(snippet.instructions) == 0

    slots = snippet.slots
    assert len(slots) == 1

    slot = slots[0]
    assert slot.name == b"code"
    assert slot.type.name == b"u32"

    assert isinstance(slot.bind, tree.snippet.Binding)
    assert slot.bind.name == b"imm"


def can_parse_snippets_with_clobbers():
    snippet = parse_snippet("asm aux() clobbers rax, rbx { mov rax, rbx; }")

    assert snippet.name == b"aux"
    assert snippet.noreturn is False
    assert len(snippet.clobbers) == 2

    assert snippet.clobbers[0].name == b"rax"
    assert snippet.clobbers[1].name == b"rbx"

    assert len(snippet.instructions) == 1
    instruction = snippet.instructions[0]

    assert instruction.mnemonic.name == b"mov"
    assert len(instruction.operands) == 2


def can_parse_snippets_with_no_return():
    snippet = parse_snippet("asm halt() noreturn { syscall; }")

    assert snippet.name == b"halt"
    assert snippet.noreturn is True

    assert len(snippet.instructions) == 1
    instruction = snippet.instructions[0]

    assert instruction.mnemonic.name == b"syscall"
    assert len(instruction.operands) == 0


def can_parse_snippets_with_no_return_with_clobbers():
    snippet = parse_snippet("asm halt() noreturn clobbers rax { syscall; }")

    assert snippet.name == b"halt"
    assert snippet.noreturn is True

    clobbers = snippet.clobbers
    assert len(clobbers) == 1
    assert clobbers[0].name == b"rax"

    assert len(snippet.instructions) == 1
    instruction = snippet.instructions[0]

    assert instruction.mnemonic.name == b"syscall"
    assert len(instruction.operands) == 0


def can_parse_snippet_with_ranged_parameter():
    snippet = parse_snippet("asm main(value@rdi: u8[0x10..0x20]) { }")

    assert len(snippet.slots) == 1

    slot = snippet.slots[0]
    assert slot.name == b"value"
    assert slot.type.name == b"u8"
    assert slot.type.range is not None
    assert slot.type.range.lower.hex() == "0x10"
    assert slot.type.range.upper.hex() == "0x20"


def can_handle_snippet_missing_slot_comma():
    code = open_text("asm exit(code@rdi: u32 id@rax: u16) { syscall; }")

    tokens = tokenize(code)
    assert isinstance(tokens, Ok)

    program = parse(code, tokens.value)
    assert isinstance(program, Err)

    diagnostics = program.error
    assert len(diagnostics) == 1

    diagnostic = diagnostics[0]
    assert diagnostic.code == "E2001"
    assert diagnostic.ref.offset == 23  # offset of "id"
    assert diagnostic.ref.length == 2  # length of "id"

def can_detect_duplicated_flags_noreturn_with_clobbers_after():
    code = open_text("asm halt() noreturn noreturn clobbers rax { syscall; }")

    tokens = tokenize(code)
    assert isinstance(tokens, Ok)

    program = parse(code, tokens.value)
    assert isinstance(program, Err)

    diagnostics = program.error
    assert len(diagnostics) == 1

    diagnostic = diagnostics[0]
    assert diagnostic.code == "E2003"
    assert diagnostic.ref.offset == 20  # offset of 2nd "noreturn"
    assert diagnostic.ref.length == 8  # length of 2nd "noreturn"



def can_detect_duplicated_flags_clobbers():
    code = open_text("asm aux() clobbers rax clobbers rcx { mov rax, rbx; }")

    tokens = tokenize(code)
    assert isinstance(tokens, Ok)

    program = parse(code, tokens.value)
    assert isinstance(program, Err)

    diagnostics = program.error
    assert len(diagnostics) == 1

    diagnostic = diagnostics[0]
    assert diagnostic.code == "E2003"
    assert diagnostic.ref.offset == 23  # offset of 2nd "clobbers"
    assert diagnostic.ref.length == 8  # length of 2nd "clobbers"


def can_detect_duplicated_flags_noreturn():
    code = open_text("asm halt() noreturn noreturn { syscall; }")

    tokens = tokenize(code)
    assert isinstance(tokens, Ok)

    program = parse(code, tokens.value)
    assert isinstance(program, Err)

    diagnostics = program.error
    assert len(diagnostics) == 1

    diagnostic = diagnostics[0]
    assert diagnostic.code == "E2003"
    assert diagnostic.ref.offset == 20  # offset of 2nd "noreturn"
    assert diagnostic.ref.length == 8  # length of 2nd "noreturn
