from i13c.semantic.typing.resolutions.addresses import AddressAcceptance
from i13c.semantic.typing.resolutions.immediates import ImmediateAcceptance
from i13c.semantic.typing.resolutions.references import ReferenceAcceptance
from i13c.semantic.typing.resolutions.registers import RegisterAcceptance
from i13c.semantic.typing.resolutions.slots import SlotAcceptance
from tests.semantic.nodes.resolutions import prepare_resolutions, prepare_rules


def can_accept_an_operand_from_a_register():
    source, resolutions = prepare_resolutions(
        """
            asm main() { call rax; }
        """
    )

    assert resolutions.operands is not None
    assert resolutions.operands.size() == 1
    id, resolution = resolutions.operands.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].kind == "register"

    assert isinstance(resolution.accepted[0].target, RegisterAcceptance)

    assert resolution.accepted[0].target.name == b"rax"
    assert resolution.accepted[0].target.kind == "64bit"
    assert resolution.accepted[0].target.width == 64

    assert source.extract(resolution.accepted[0].ref) == b"rax"


def can_accept_an_operand_from_an_immediate():
    source, resolutions = prepare_resolutions(
        """
            asm main() { call 0x1234; }
        """
    )

    assert resolutions.operands is not None
    assert resolutions.operands.size() == 1
    id, resolution = resolutions.operands.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].kind == "immediate"

    assert isinstance(resolution.accepted[0].target, ImmediateAcceptance)
    assert resolution.accepted[0].target.value.data.hex() == "1234"
    assert resolution.accepted[0].target.value.width == 16

    assert source.extract(resolution.accepted[0].ref) == b"0x1234"


def can_accept_an_operand_from_a_reference():
    source, resolutions = prepare_resolutions(
        """
            asm main(x@rax: u16) { call @x; }
        """
    )

    assert resolutions.operands is not None
    assert resolutions.operands.size() == 1
    id, resolution = resolutions.operands.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].kind == "reference"

    assert isinstance(resolution.accepted[0].target, ReferenceAcceptance)
    assert resolution.accepted[0].target.name == b"x"
    assert isinstance(resolution.accepted[0].target.target, SlotAcceptance)

    assert source.extract(resolution.accepted[0].ref) == b"@x"


def can_accept_an_operand_from_an_address():
    source, resolutions = prepare_resolutions(
        """
            asm main() { call [rax]; }
        """
    )

    assert resolutions.operands is not None
    assert resolutions.operands.size() == 1
    id, resolution = resolutions.operands.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].kind == "address"

    assert isinstance(resolution.accepted[0].target, AddressAcceptance)
    assert isinstance(resolution.accepted[0].target.base, RegisterAcceptance)

    assert resolution.accepted[0].target.base.kind == "64bit"
    assert resolution.accepted[0].target.base.name == b"rax"
    assert resolution.accepted[0].target.base.width == 64
    assert resolution.accepted[0].target.offset is None

    assert source.extract(resolution.accepted[0].ref) == b"[rax]"


def can_accept_an_operand_from_an_address_using_a_reference_as_base():
    source, resolutions = prepare_resolutions(
        """
            asm main(x@rax: u16) { call [@x + 0x0f]; }
        """
    )

    assert resolutions.operands is not None
    assert resolutions.operands.size() == 1
    id, resolution = resolutions.operands.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].kind == "address"

    assert isinstance(resolution.accepted[0].target, AddressAcceptance)
    assert isinstance(resolution.accepted[0].target.base, ReferenceAcceptance)

    assert resolution.accepted[0].target.offset is not None
    assert resolution.accepted[0].target.base.name == b"x"

    assert isinstance(resolution.accepted[0].target.base.target, SlotAcceptance)
    assert resolution.accepted[0].target.base.target.name == b"x"
    assert resolution.accepted[0].target.base.target.bind.mode == "register"
    assert resolution.accepted[0].target.base.target.bind.target == b"rax"

    assert source.extract(resolution.accepted[0].ref) == b"[@x + 0x0f]"


def can_reject_rip_register():
    source, resolutions = prepare_resolutions(
        """
            asm main() { call rip; }
        """
    )

    assert resolutions.operands is not None
    assert resolutions.operands.size() == 1
    _, resolution = resolutions.operands.peak()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].kind == "register"
    assert resolution.rejected[0].reason == "unsupported-register"

    assert source.extract(resolution.rejected[0].ref) == b"rip"


def can_detect_a_broken_range_rule_e3021():
    _, rules = prepare_rules(
        """
            asm main() { call rip; }
        """
    )

    assert len(rules.get("e3021")) == 1
