from i13c.semantic.typing.resolutions.parameters import ParameterAcceptance
from i13c.semantic.typing.resolutions.values import ValueAcceptance
from tests.semantic.nodes.resolutions import prepare_resolutions, prepare_rules


def can_accept_valid_expression_from_value():
    source, resolutions = prepare_resolutions(
        """
            fn main() { val x: u16 = 0x1234; val y: u16 = x; }
        """
    )

    assert resolutions.expressions is not None
    assert resolutions.expressions.size() == 1
    id, resolution = resolutions.expressions.peek()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert isinstance(resolution.accepted[0].target, ValueAcceptance)

    assert resolution.accepted[0].target.name == b"x"
    assert b"x" in resolution.accepted[0].environment

    assert source.extract(resolution.accepted[0].ref) == b"x"


def can_accept_valid_expression_from_parameter():
    source, resolutions = prepare_resolutions(
        """
            fn main(x: u16) { val y: u16 = x; }
        """
    )

    assert resolutions.expressions is not None
    assert resolutions.expressions.size() == 1
    id, resolution = resolutions.expressions.peek()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert isinstance(resolution.accepted[0].target, ParameterAcceptance)

    assert resolution.accepted[0].target.name == b"x"
    assert b"x" in resolution.accepted[0].environment

    assert source.extract(resolution.accepted[0].ref) == b"x"


def can_rejected_unresolved_expression():
    source, resolutions = prepare_resolutions(
        """
            fn main() { val y: u16 = x; }
        """
    )

    assert resolutions.expressions is not None
    assert resolutions.expressions.size() == 1
    id, resolution = resolutions.expressions.peek()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].id == id
    assert resolution.rejected[0].name == b"x"
    assert resolution.rejected[0].reason == "unresolved"

    assert source.extract(resolution.rejected[0].ref) == b"x"


def can_detect_an_unresolved_expression():
    _, rules = prepare_rules(
        """
            fn main() { val y: u16 = x; }
        """
    )

    assert len(rules.get("e3010")) == 1
