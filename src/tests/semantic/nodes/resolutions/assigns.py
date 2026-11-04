from i13c.semantic.typing.resolutions.callsites import CallSiteAcceptance
from i13c.semantic.typing.resolutions.literals import LiteralAcceptance
from i13c.semantic.typing.resolutions.parameters import ParameterAcceptance
from i13c.semantic.typing.resolutions.usages import UsageAcceptance
from tests.semantic.nodes.resolutions import prepare_resolutions, prepare_rules


def can_accept_valid_assign_from_literal():
    source, resolutions = prepare_resolutions(
        """
            fn main() { val x: u16 = 0x1234; }
        """
    )

    assert resolutions.assigns is not None
    assert resolutions.assigns.size() == 1
    id, resolution = resolutions.assigns.peek()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].destination.name == b"x"

    assert resolution.accepted[0].destination.type.width == 16
    assert resolution.accepted[0].destination.type.range is None

    assert isinstance(resolution.accepted[0].expression, LiteralAcceptance)
    assert resolution.accepted[0].expression.target.data.hex() == "1234"
    assert resolution.accepted[0].expression.target.width == 16

    assert source.extract(resolution.accepted[0].ref) == b"x: u16 = 0x1234"


def can_accept_valid_assign_from_parameter():
    source, resolutions = prepare_resolutions(
        """
            fn main(v: u16) { val x: u16 = v; }
        """
    )

    assert resolutions.assigns is not None
    assert resolutions.assigns.size() == 1
    id, resolution = resolutions.assigns.peek()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].destination.name == b"x"

    assert resolution.accepted[0].destination.type.width == 16
    assert resolution.accepted[0].destination.type.range is None

    assert isinstance(resolution.accepted[0].expression, UsageAcceptance)
    assert resolution.accepted[0].expression.name == b"v"

    assert b"v" in resolution.accepted[0].expression.environment
    entry = resolution.accepted[0].expression.environment[b"v"]

    assert isinstance(entry, ParameterAcceptance)
    assert entry.type.name == b"u16"
    assert entry.type.width == 16

    assert source.extract(resolution.accepted[0].ref) == b"x: u16 = v"


def can_accept_valid_assign_from_callsite():
    source, resolutions = prepare_resolutions(
        """
            asm foo() -> u16@rax { }
            fn main() { val x: u16 = foo(); }
        """
    )

    assert resolutions.assigns is not None
    assert resolutions.assigns.size() == 1
    id, resolution = resolutions.assigns.peek()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].destination.name == b"x"
    assert resolution.accepted[0].destination.type.width == 16

    assert isinstance(resolution.accepted[0].expression, CallSiteAcceptance)
    assert resolution.accepted[0].expression.signature.name == b"foo"

    assert resolution.accepted[0].expression.signature.result is not None
    assert resolution.accepted[0].expression.signature.result.type.name == b"u16"
    assert resolution.accepted[0].expression.signature.result.type.width == 16

    assert source.extract(resolution.accepted[0].ref) == b"x: u16 = foo()"


def can_accept_valid_assign_from_callsite_with_arguments():
    source, resolutions = prepare_resolutions(
        """
            asm foo(a@rdi: u8) -> u16@rax { }
            fn main() { val x: u16 = foo(0x12); }
        """
    )

    assert resolutions.assigns is not None
    assert resolutions.assigns.size() == 1
    id, resolution = resolutions.assigns.peek()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert isinstance(resolution.accepted[0].expression, CallSiteAcceptance)
    assert resolution.accepted[0].expression.signature.name == b"foo"

    assert source.extract(resolution.accepted[0].ref) == b"x: u16 = foo(0x12)"


def can_accept_valid_assign_from_callsite_with_narrower_range():
    source, resolutions = prepare_resolutions(
        """
            asm foo() -> u8[0x01..0x02]@rax { }
            fn main() { val x: u8[0x00..0x03] = foo(); }
        """
    )

    assert resolutions.assigns is not None
    assert resolutions.assigns.size() == 1
    id, resolution = resolutions.assigns.peek()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert isinstance(resolution.accepted[0].expression, CallSiteAcceptance)

    assert source.extract(resolution.accepted[0].ref) == b"x: u8[0x00..0x03] = foo()"


def can_accept_valid_assign_from_literal_in_range():
    source, resolutions = prepare_resolutions(
        """
            fn main() { val x: u8[0x01..0x02] = 0x02; }
        """
    )

    assert resolutions.assigns is not None
    assert resolutions.assigns.size() == 1
    id, resolution = resolutions.assigns.peek()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert isinstance(resolution.accepted[0].expression, LiteralAcceptance)

    assert source.extract(resolution.accepted[0].ref) == b"x: u8[0x01..0x02] = 0x02"


def can_reject_assign_from_literal_with_unmatched_width():
    source, resolutions = prepare_resolutions(
        """
            fn main() { val x: u8 = 0x1234; }
        """
    )

    assert resolutions.assigns is not None
    assert resolutions.assigns.size() == 1
    id, resolution = resolutions.assigns.peek()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].id == id
    assert resolution.rejected[0].reason == "type-mismatch"
    assert source.extract(resolution.rejected[0].ref) == b"x: u8 = 0x1234"


def can_reject_assign_from_literal_out_of_range():
    source, resolutions = prepare_resolutions(
        """
            fn main() { val x: u8[0x01..0x02] = 0x03; }
        """
    )

    assert resolutions.assigns is not None
    assert resolutions.assigns.size() == 1
    id, resolution = resolutions.assigns.peek()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].id == id
    assert resolution.rejected[0].reason == "type-mismatch"
    assert source.extract(resolution.rejected[0].ref) == b"x: u8[0x01..0x02] = 0x03"


def can_reject_assign_from_parameter_with_unmatched_width():
    source, resolutions = prepare_resolutions(
        """
            fn main(v: u16) { val x: u8 = v; }
        """
    )

    assert resolutions.assigns is not None
    assert resolutions.assigns.size() == 1
    id, resolution = resolutions.assigns.peek()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].id == id
    assert resolution.rejected[0].reason == "type-mismatch"
    assert source.extract(resolution.rejected[0].ref) == b"x: u8 = v"


def can_reject_assign_from_parameter_with_wider_range():
    source, resolutions = prepare_resolutions(
        """
            fn main(v: u8) { val x: u8[0x01..0x02] = v; }
        """
    )

    assert resolutions.assigns is not None
    assert resolutions.assigns.size() == 1
    id, resolution = resolutions.assigns.peek()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].id == id
    assert resolution.rejected[0].reason == "type-mismatch"
    assert source.extract(resolution.rejected[0].ref) == b"x: u8[0x01..0x02] = v"


def can_reject_assign_from_value_with_unmatched_width():
    source, resolutions = prepare_resolutions(
        """
            fn main() { val v: u16 = 0x1234; val x: u8 = v; }
        """
    )

    assert resolutions.assigns is not None
    assert resolutions.assigns.size() == 2

    # only the second assign is expected to be rejected
    rejected = [(k, v) for k, v in resolutions.assigns.items() if v.rejected]
    assert len(rejected) == 1
    id, resolution = rejected[0]

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].id == id
    assert resolution.rejected[0].reason == "type-mismatch"
    assert source.extract(resolution.rejected[0].ref) == b"x: u8 = v"


def can_reject_assign_from_callsite_with_unmatched_width():
    source, resolutions = prepare_resolutions(
        """
            asm foo() -> u16@rax { }
            fn main() { val x: u8 = foo(); }
        """
    )

    assert resolutions.assigns is not None
    assert resolutions.assigns.size() == 1
    id, resolution = resolutions.assigns.peek()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].id == id
    assert resolution.rejected[0].reason == "type-mismatch"
    assert source.extract(resolution.rejected[0].ref) == b"x: u8 = foo()"


def can_reject_assign_from_callsite_with_wider_range():
    source, resolutions = prepare_resolutions(
        """
            asm foo() -> u8@rax { }
            fn main() { val x: u8[0x01..0x02] = foo(); }
        """
    )

    assert resolutions.assigns is not None
    assert resolutions.assigns.size() == 1
    id, resolution = resolutions.assigns.peek()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].id == id
    assert resolution.rejected[0].reason == "type-mismatch"
    assert source.extract(resolution.rejected[0].ref) == b"x: u8[0x01..0x02] = foo()"


def can_reject_assign_from_snippet_callsite_without_result():
    source, resolutions = prepare_resolutions(
        """
            asm foo() { }
            fn main() { val x: u8 = foo(); }
        """
    )

    assert resolutions.assigns is not None
    assert resolutions.assigns.size() == 1
    id, resolution = resolutions.assigns.peek()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].id == id
    assert resolution.rejected[0].reason == "type-mismatch"
    assert source.extract(resolution.rejected[0].ref) == b"x: u8 = foo()"


def can_reject_assign_from_function_callsite_without_result():
    source, resolutions = prepare_resolutions(
        """
            fn foo() { }
            fn main() { val x: u8 = foo(); }
        """
    )

    assert resolutions.assigns is not None
    assert resolutions.assigns.size() == 1
    id, resolution = resolutions.assigns.peek()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].id == id
    assert resolution.rejected[0].reason == "type-mismatch"
    assert source.extract(resolution.rejected[0].ref) == b"x: u8 = foo()"


def can_detect_unmatched_assign_type_rule_e3007():
    _, rules = prepare_rules(
        """
            fn main() { val x: u8 = 0x1234; }
        """
    )

    assert len(rules.get("e3007")) == 1
