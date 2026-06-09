from i13c.semantic.typing.analyses.asmlets import Asmlet
from i13c.semantic.typing.resolutions.callsites import CallSiteAcceptance
from i13c.semantic.typing.resolutions.literals import LiteralAcceptance
from tests.semantic.nodes.analyses import prepare_analyses


def can_do_nothing_without_any_callsite():
    _, analyses = prepare_analyses("""
        fn main() { }
    """)

    assert analyses.callings is not None
    assert analyses.callings.size() == 0


def can_resolve_callsite_to_function():
    _, analyses = prepare_analyses("""
        fn main() { foo(); }
        fn foo() { }
    """)

    assert analyses.callings is not None
    assert analyses.callings.size() == 1
    _, calling = analyses.callings.peak()

    assert calling.signature.name == b"foo"
    assert isinstance(calling.target, CallSiteAcceptance)

    assert len(calling.arguments) == 0
    assert len(calling.parameters) == 0


def can_resolve_callsite_to_function_with_parameters():
    _, analyses = prepare_analyses("""
        fn main() { foo(0x42); }
        fn foo(x: u8) { }
    """)

    assert analyses.callings is not None
    assert analyses.callings.size() == 1
    _, calling = analyses.callings.peak()

    assert calling.signature.name == b"foo"
    assert isinstance(calling.target, CallSiteAcceptance)

    assert len(calling.parameters) == 1
    assert calling.parameters[0].name == b"x"
    assert calling.parameters[0].type.name == b"u8"

    assert len(calling.arguments) == 1
    assert isinstance(calling.arguments[0], LiteralAcceptance)
    assert str(calling.arguments[0].target) == "0x42"


def can_resolve_callsite_to_asmlet():
    _, analyses = prepare_analyses("""
        asm foo() { }
        fn main() { foo(); }
    """)

    assert analyses.callings is not None
    assert analyses.callings.size() == 1
    _, calling = analyses.callings.peak()

    assert calling.signature.name == b"foo"
    assert isinstance(calling.target, Asmlet)

    assert len(calling.arguments) == 0
    assert len(calling.parameters) == 0


def can_resolve_callsite_to_asmlet_with_parameters():
    _, analyses = prepare_analyses("""
        asm foo(x@rdi: u8) { }
        fn main() { foo(0x42); }
    """)

    assert analyses.callings is not None
    assert analyses.callings.size() == 1
    _, calling = analyses.callings.peak()

    assert calling.signature.name == b"foo"
    assert isinstance(calling.target, Asmlet)

    assert len(calling.parameters) == 1
    assert calling.parameters[0].name == b"x"
    assert calling.parameters[0].type.name == b"u8"

    assert len(calling.arguments) == 1
    assert isinstance(calling.arguments[0], LiteralAcceptance)
    assert str(calling.arguments[0].target) == "0x42"


def can_resolve_callsite_to_asmlet_reduced():
    _, analyses = prepare_analyses("""
        asm foo(x@imm: u8) { }
        fn main() { foo(0x42); }
    """)

    assert analyses.callings is not None
    assert analyses.callings.size() == 1
    _, calling = analyses.callings.peak()

    assert calling.signature.name == b"foo"
    assert isinstance(calling.target, Asmlet)

    assert len(calling.parameters) == 0
    assert len(calling.arguments) == 0


def can_resolve_callsite_to_asmlet_reduced_twiced():
    _, analyses = prepare_analyses("""
        asm foo(x@imm: u8) { }
        fn main() { foo(0x42); foo(0x17); }
    """)

    assert analyses.callings is not None
    assert analyses.callings.size() == 2

    for calling in analyses.callings.values():
        assert calling.signature.name == b"foo"
        assert isinstance(calling.target, Asmlet)

        assert len(calling.parameters) == 0
        assert len(calling.arguments) == 0
