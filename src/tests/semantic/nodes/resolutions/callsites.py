from tests.semantic.nodes.resolutions import prepare_resolutions, prepare_rules


def can_accept_an_empty_function():
    _, resolutions = prepare_resolutions(
        """
            fn main() { }
        """
    )

    assert resolutions.callsites is not None
    assert resolutions.callsites.size() == 0


def can_accept_an_empty_resolved_call():
    source, resolutions = prepare_resolutions(
        """
            fn foo() { }
            fn main() { foo(); }
        """
    )

    assert resolutions.callsites is not None
    assert resolutions.callsites.size() == 1
    id, resolution = resolutions.callsites.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].target.name == b"foo"
    assert len(resolution.accepted[0].target.parameters) == 0

    assert source.extract(resolution.accepted[0].ref) == b"foo()"


def can_accept_a_call_with_literal():
    source, resolutions = prepare_resolutions(
        """
            fn foo(x: u8) { }
            fn main() { foo(0x42); }
        """
    )

    assert resolutions.callsites is not None
    assert resolutions.callsites.size() == 1
    id, resolution = resolutions.callsites.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].target.name == b"foo"

    assert len(resolution.accepted[0].target.parameters) == 1
    assert resolution.accepted[0].target.parameters[0].name == b"x"

    assert source.extract(resolution.accepted[0].ref) == b"foo(0x42)"


def can_accept_a_call_with_literal_ranged():
    source, resolutions = prepare_resolutions(
        """
            fn foo(x: u8[0x01..0x02]) { }
            fn main() { foo(0x01); }
        """
    )

    assert resolutions.callsites is not None
    assert resolutions.callsites.size() == 1
    id, resolution = resolutions.callsites.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].target.name == b"foo"

    assert len(resolution.accepted[0].target.parameters) == 1
    assert resolution.accepted[0].target.parameters[0].name == b"x"

    assert source.extract(resolution.accepted[0].ref) == b"foo(0x01)"


def can_accept_a_call_with_parameter():
    source, resolutions = prepare_resolutions(
        """
            fn foo(x: u8) { }
            fn main(y: u8) { foo(y); }
        """
    )

    assert resolutions.callsites is not None
    assert resolutions.callsites.size() == 1
    id, resolution = resolutions.callsites.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].target.name == b"foo"

    assert len(resolution.accepted[0].target.parameters) == 1
    assert resolution.accepted[0].target.parameters[0].name == b"x"

    assert source.extract(resolution.accepted[0].ref) == b"foo(y)"


def can_accept_a_call_with_parameter_ranged():
    source, resolutions = prepare_resolutions(
        """
            fn foo(x: u8[0x01..0x03]) { }
            fn main(y: u8[0x01..0x02]) { foo(y); }
        """
    )

    assert resolutions.callsites is not None
    assert resolutions.callsites.size() == 1
    id, resolution = resolutions.callsites.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].target.name == b"foo"

    assert len(resolution.accepted[0].target.parameters) == 1
    assert resolution.accepted[0].target.parameters[0].name == b"x"

    assert source.extract(resolution.accepted[0].ref) == b"foo(y)"


def can_accept_a_call_with_expression():
    source, resolutions = prepare_resolutions(
        """
            fn foo(x: u8) { }
            fn main() { val y: u8 = 0x01; foo(y); }
        """
    )

    assert resolutions.callsites is not None
    assert resolutions.callsites.size() == 1
    id, resolution = resolutions.callsites.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].target.name == b"foo"

    assert len(resolution.accepted[0].target.parameters) == 1
    assert resolution.accepted[0].target.parameters[0].name == b"x"

    assert source.extract(resolution.accepted[0].ref) == b"foo(y)"


def can_accept_a_call_with_multiple_arguments():
    source, resolutions = prepare_resolutions(
        """
            fn foo(x: u8, y: u16, z: u32) { }
            fn main(b: u32) { val a: u16 = 0x0001; foo(0x01, a, b); }
        """
    )

    assert resolutions.callsites is not None
    assert resolutions.callsites.size() == 1
    id, resolution = resolutions.callsites.peak()

    assert len(resolution.accepted) == 1
    assert len(resolution.rejected) == 0

    assert resolution.accepted[0].id == id
    assert resolution.accepted[0].target.name == b"foo"

    assert len(resolution.accepted[0].target.parameters) == 3
    assert resolution.accepted[0].target.parameters[0].name == b"x"
    assert resolution.accepted[0].target.parameters[1].name == b"y"
    assert resolution.accepted[0].target.parameters[2].name == b"z"

    assert source.extract(resolution.accepted[0].ref) == b"foo(0x01, a, b)"


def can_reject_a_call_with_unknown_target():
    source, resolutions = prepare_resolutions(
        """
            fn main() { bar(); }
        """
    )

    assert resolutions.callsites is not None
    assert resolutions.callsites.size() == 1
    _, resolution = resolutions.callsites.peak()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].reason == "unknown-target"
    assert source.extract(resolution.rejected[0].ref) == b"bar()"


def can_reject_a_call_with_unmatched_arity():
    source, resolutions = prepare_resolutions(
        """
            fn foo(x: u8) { }
            fn main() { foo(0x01, 0x02); }
        """
    )

    assert resolutions.callsites is not None
    assert resolutions.callsites.size() == 1
    _, resolution = resolutions.callsites.peak()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].reason == "arity-mismatch"
    assert source.extract(resolution.rejected[0].ref) == b"foo(0x01, 0x02)"


def can_reject_a_call_with_unmatched_literal_type():
    source, resolutions = prepare_resolutions(
        """
            fn foo(x: u8) { }
            fn main() { foo(0x0001); }
        """
    )

    assert resolutions.callsites is not None
    assert resolutions.callsites.size() == 1
    _, resolution = resolutions.callsites.peak()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].reason == "type-mismatch"
    assert source.extract(resolution.rejected[0].ref) == b"foo(0x0001)"


def can_reject_a_call_with_unmatched_literal_type_lower_bound():
    source, resolutions = prepare_resolutions(
        """
            fn foo(x: u8[0x01..0x02]) { }
            fn main() { foo(0x00); }
        """
    )

    assert resolutions.callsites is not None
    assert resolutions.callsites.size() == 1
    _, resolution = resolutions.callsites.peak()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].reason == "type-mismatch"
    assert source.extract(resolution.rejected[0].ref) == b"foo(0x00)"


def can_reject_a_call_with_unmatched_literal_type_upper_bound():
    source, resolutions = prepare_resolutions(
        """
            fn foo(x: u8[0x01..0x02]) { }
            fn main() { foo(0x03); }
        """
    )

    assert resolutions.callsites is not None
    assert resolutions.callsites.size() == 1
    _, resolution = resolutions.callsites.peak()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].reason == "type-mismatch"
    assert source.extract(resolution.rejected[0].ref) == b"foo(0x03)"


def can_reject_a_call_with_unmatched_parameter_type():
    source, resolutions = prepare_resolutions(
        """
            fn foo(x: u8) { }
            fn main(y: u16) { foo(y); }
        """
    )

    assert resolutions.callsites is not None
    assert resolutions.callsites.size() == 1
    _, resolution = resolutions.callsites.peak()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].reason == "type-mismatch"
    assert source.extract(resolution.rejected[0].ref) == b"foo(y)"


def can_reject_a_call_with_unmatched_parameter_type_lower_bound():
    source, resolutions = prepare_resolutions(
        """
            fn foo(x: u8[0x01..0x02]) { }
            fn main(y: u8[0x00..0x02]) { foo(y); }
        """
    )

    assert resolutions.callsites is not None
    assert resolutions.callsites.size() == 1
    _, resolution = resolutions.callsites.peak()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].reason == "type-mismatch"
    assert source.extract(resolution.rejected[0].ref) == b"foo(y)"


def can_reject_a_call_with_unmatched_parameter_type_upper_bound():
    source, resolutions = prepare_resolutions(
        """
            fn foo(x: u8[0x01..0x02]) { }
            fn main(y: u8[0x01..0x03]) { foo(y); }
        """
    )

    assert resolutions.callsites is not None
    assert resolutions.callsites.size() == 1
    _, resolution = resolutions.callsites.peak()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].reason == "type-mismatch"
    assert source.extract(resolution.rejected[0].ref) == b"foo(y)"


def can_reject_a_call_with_unmatched_expression_type():
    source, resolutions = prepare_resolutions(
        """
            fn foo(x: u8) { }
            fn main() { val y: u16 = 0x0001; foo(y); }
        """
    )

    assert resolutions.callsites is not None
    assert resolutions.callsites.size() == 1
    _, resolution = resolutions.callsites.peak()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].reason == "type-mismatch"
    assert source.extract(resolution.rejected[0].ref) == b"foo(y)"


def can_reject_a_call_with_unmatched_expression_type_lower_bound():
    source, resolutions = prepare_resolutions(
        """
            fn foo(x: u8[0x01..0x02]) { }
            fn main() { val y: u8[0x00..0x02] = 0x00; foo(y); }
        """
    )

    assert resolutions.callsites is not None
    assert resolutions.callsites.size() == 1
    _, resolution = resolutions.callsites.peak()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].reason == "type-mismatch"
    assert source.extract(resolution.rejected[0].ref) == b"foo(y)"


def can_reject_a_call_with_unmatched_expression_type_upper_bound():
    source, resolutions = prepare_resolutions(
        """
            fn foo(x: u8[0x01..0x02]) { }
            fn main() { val y: u8[0x01..0x03] = 0x03; foo(y); }
        """
    )

    assert resolutions.callsites is not None
    assert resolutions.callsites.size() == 1
    _, resolution = resolutions.callsites.peak()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].reason == "type-mismatch"
    assert source.extract(resolution.rejected[0].ref) == b"foo(y)"


def can_reject_a_call_with_unmatched_3rd_argument():
    source, resolutions = prepare_resolutions(
        """
            fn foo(x: u8, y: u16, z: u32) { }
            fn main(a: u8, b: u16, c: u64) { foo(a, b, c); }
        """
    )

    assert resolutions.callsites is not None
    assert resolutions.callsites.size() == 1
    _, resolution = resolutions.callsites.peak()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].reason == "type-mismatch"
    assert source.extract(resolution.rejected[0].ref) == b"foo(a, b, c)"


def can_reject_a_call_with_unresolved_symbol():
    source, resolutions = prepare_resolutions(
        """
            fn foo(x: u8) { }
            fn main() { foo(bar); }
        """
    )

    assert resolutions.callsites is not None
    assert resolutions.callsites.size() == 1
    _, resolution = resolutions.callsites.peak()

    assert len(resolution.accepted) == 0
    assert len(resolution.rejected) == 1

    assert resolution.rejected[0].reason == "unknown-target"
    assert source.extract(resolution.rejected[0].ref) == b"foo(bar)"


def can_detect_a_broken_range_rule_e3006():
    _, rules = prepare_rules(
        """
            fn foo(x: u8[0x01..0x02]) { }
            fn main() { foo(0x03); }
        """
    )

    assert len(rules.get("e3006")) == 1
