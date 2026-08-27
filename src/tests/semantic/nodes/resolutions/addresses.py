from i13c.semantic.typing.resolutions.parameters import ParameterAcceptance
from i13c.semantic.typing.resolutions.registers import RegisterAcceptance
from tests.semantic.nodes.resolutions import prepare_resolutions, prepare_rules


def can_accept_an_offsetless_address():
    source, resolutions = prepare_resolutions("""
        asm main() { jmp [rax]; }
    """)

    assert resolutions.addresses is not None
    assert resolutions.addresses.size() == 1
    id, resolution = resolutions.addresses.peek()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].base.name == b"rax"
    assert resolution.accepted[0].offset is None

    assert isinstance(resolution.accepted[0].base, RegisterAcceptance)
    assert resolution.accepted[0].base.kind == "64bit"
    assert resolution.accepted[0].base.width == 64

    assert source.extract(resolution.accepted[0].ref) == b"[rax]"


def can_accept_an_indexed_address():
    source, resolutions = prepare_resolutions("""
        asm main() { jmp [rax + rbx]; }
    """)

    assert resolutions.addresses is not None
    assert resolutions.addresses.size() == 1
    id, resolution = resolutions.addresses.peek()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].base.name == b"rax"
    assert resolution.accepted[0].offset is None

    assert resolution.accepted[0].indx is not None
    assert resolution.accepted[0].indx.name == b"rbx"

    assert isinstance(resolution.accepted[0].base, RegisterAcceptance)
    assert resolution.accepted[0].base.kind == "64bit"
    assert resolution.accepted[0].base.width == 64

    assert source.extract(resolution.accepted[0].ref) == b"[rax + rbx]"



def can_accept_a_forward_address():
    source, resolutions = prepare_resolutions("""
        asm main() { jmp [rax + 0x0300]; }
    """)

    assert resolutions.addresses is not None
    assert resolutions.addresses.size() == 1
    id, resolution = resolutions.addresses.peek()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].base.name == b"rax"

    assert resolution.accepted[0].offset is not None
    assert resolution.accepted[0].offset.kind == "forward"

    assert resolution.accepted[0].offset.imm.value.width == 16
    assert resolution.accepted[0].offset.imm.value.data.hex() == "0300"

    assert isinstance(resolution.accepted[0].base, RegisterAcceptance)
    assert resolution.accepted[0].base.kind == "64bit"
    assert resolution.accepted[0].base.width == 64

    assert source.extract(resolution.accepted[0].ref) == b"[rax + 0x0300]"


def can_accept_a_backward_address():
    source, resolutions = prepare_resolutions("""
        asm main() { jmp [rax - 0x0300]; }
    """)

    assert resolutions.addresses is not None
    assert resolutions.addresses.size() == 1
    id, resolution = resolutions.addresses.peek()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].base.name == b"rax"

    assert isinstance(resolution.accepted[0].base, RegisterAcceptance)
    assert resolution.accepted[0].base.kind == "64bit"
    assert resolution.accepted[0].base.width == 64

    assert resolution.accepted[0].offset is not None
    assert resolution.accepted[0].offset.kind == "backward"

    assert resolution.accepted[0].offset.imm.value.width == 16
    assert resolution.accepted[0].offset.imm.value.data.hex() == "0300"

    assert source.extract(resolution.accepted[0].ref) == b"[rax - 0x0300]"


def can_accept_register_bound_param_as_the_base():
    source, resolutions = prepare_resolutions("""
        asm main(v@rax: u64) { jmp [@v]; }
    """)

    assert resolutions.addresses is not None
    assert resolutions.addresses.size() == 1
    id, resolution = resolutions.addresses.peek()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].base.name == b"v"
    assert resolution.accepted[0].offset is None

    assert isinstance(resolution.accepted[0].base, ParameterAcceptance)
    assert resolution.accepted[0].base.name == b"v"
    assert resolution.accepted[0].base.type.width == 64
    assert resolution.accepted[0].base.type.name == b"u64"

    assert source.extract(resolution.accepted[0].ref) == b"[@v]"


def can_reject_immediate_bound_param_as_the_base():
    source, resolutions = prepare_resolutions("""
        asm main(v@imm: u64) { jmp [@v]; }
    """)

    assert resolutions.addresses is not None
    assert resolutions.addresses.size() == 1
    _, resolution = resolutions.addresses.peek()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].reason == "invalid-register"
    assert source.extract(resolution.rejected[0].ref) == b"[@v]"


def can_reject_rip_register():
    source, resolutions = prepare_resolutions("""
        asm main() { jmp [rip]; }
    """)

    assert resolutions.addresses is not None
    assert resolutions.addresses.size() == 1
    _, resolution = resolutions.addresses.peek()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].reason == "invalid-register"
    assert source.extract(resolution.rejected[0].ref) == b"[rip]"


def can_reject_label_as_the_address_base():
    source, resolutions = prepare_resolutions("""
        asm main() { .me: jmp [@me]; }
    """)

    assert resolutions.addresses is not None
    assert resolutions.addresses.size() == 1
    _, resolution = resolutions.addresses.peek()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].reason == "invalid-register"
    assert source.extract(resolution.rejected[0].ref) == b"[@me]"


def can_reject_non_64bit_register():
    source, resolutions = prepare_resolutions("""
        asm main() { jmp [eax]; }
    """)

    assert resolutions.addresses is not None
    assert resolutions.addresses.size() == 1
    _, resolution = resolutions.addresses.peek()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].reason == "invalid-register"
    assert source.extract(resolution.rejected[0].ref) == b"[eax]"


def can_reject_forward_offset_not_eligible_for_displacement():
    source, resolutions = prepare_resolutions("""
        asm main() { jmp [rax + 0x80000000]; }
    """)

    assert resolutions.addresses is not None
    assert resolutions.addresses.size() == 1
    _, resolution = resolutions.addresses.peek()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].reason == "invalid-offset"
    assert source.extract(resolution.rejected[0].ref) == b"[rax + 0x80000000]"


def can_reject_backward_offset_not_eligible_for_displacement():
    source, resolutions = prepare_resolutions("""
        asm main() { jmp [rax - 0x80000000]; }
    """)

    assert resolutions.addresses is not None
    assert resolutions.addresses.size() == 1
    _, resolution = resolutions.addresses.peek()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].reason == "invalid-offset"
    assert source.extract(resolution.rejected[0].ref) == b"[rax - 0x80000000]"


def can_detect_a_broken_range_rule_e3022():
    _, rules = prepare_rules("""
        asm main() { jmp [rip]; }
    """)

    assert len(rules.get("e3022")) == 1
