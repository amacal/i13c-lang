from i13c.sem import model, syntax
from i13c.sem.typing.entities.callsites import CallSiteId
from i13c.sem.typing.entities.operands import Immediate, Register
from i13c.sem.typing.indices.instances import Instance
from tests.sem import prepare_program


def can_do_nothing_without_any_snippet():
    _, program = prepare_program(
        """
            fn main() noreturn { }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    instances = semantic.indices.instance_by_callsite

    assert instances.size() == 0


def can_do_nothing_without_any_callsite():
    _, program = prepare_program(
        """
            asm exit(code@imm: u8) { shl rax, code; }
            fn main() noreturn { }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    instances = semantic.indices.instance_by_callsite

    assert instances.size() == 0


def can_do_nothing_without_accepted_callsite():
    _, program = prepare_program(
        """
            asm exit(code@imm: u8) { shl rax, code; }
            fn main() noreturn { exit(0x1001); }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    instances = semantic.indices.instance_by_callsite

    assert instances.size() == 0


def can_do_nothing_with_ambiguous_callsite():
    _, program = prepare_program(
        """
            asm exit(code@imm: u8) { shl rax, code; }
            asm exit(code@imm: u64) { shl rax, code; }
            fn main() noreturn { exit(0x42); }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    instances = semantic.indices.instance_by_callsite

    assert instances.size() == 0


def can_generate_instance_for_accepted_callsite():
    _, program = prepare_program(
        """
            asm exit(code@imm: u8) { shl rax, code; }
            fn main() noreturn { exit(0x42); }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    instances = semantic.indices.instance_by_callsite

    assert instances.size() == 1
    id, value = instances.peak()

    assert isinstance(id, CallSiteId)
    assert isinstance(value, Instance)

    callsite = semantic.basic.callsites.get(id)
    assert callsite.callee.name == b"exit"

    snippet = semantic.basic.snippets.get(value.target)
    assert snippet.identifier.name == b"exit"

    # removed immedate out-of-bound argument
    assert len(value.bindings) == 0

    # rewritten operand from reference to immediate
    assert len(value.operands) == 1
    id, operand = next(iter(value.operands.items()))

    # previously was a reference to an operand
    reference = semantic.basic.operands.get(id)
    assert reference.kind == b"reference"

    # now is an immediate
    assert operand.kind == b"immediate"
    assert isinstance(operand.target, Immediate)

    # its value and with are from callsite
    assert operand.target.value == 0x42
    assert operand.target.width == 8


def can_generate_instance_with_callsite_of_multiple_arguments():
    _, program = prepare_program(
        """
            asm exit(id@rax: u64, code@imm: u8) { shl rax, code; }
            fn main() noreturn { exit(0x1234, 0x42); }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    instances = semantic.indices.instance_by_callsite

    assert instances.size() == 1
    id, value = instances.peak()

    assert isinstance(id, CallSiteId)
    assert isinstance(value, Instance)

    # kept only non-immediate argument
    assert len(value.bindings) == 1

    # rewritten one operand
    assert len(value.operands) == 1


def can_generate_instance_with_reference_used_twice():
    _, program = prepare_program(
        """
            asm exit(code@imm: u8) { shl rax, code; shl rbx, code; }
            fn main() noreturn { exit(0x42); }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    instances = semantic.indices.instance_by_callsite

    assert instances.size() == 1
    id, value = instances.peak()

    assert isinstance(id, CallSiteId)
    assert isinstance(value, Instance)

    # kept only non-immediate argument
    assert len(value.bindings) == 0

    # rewritten two operands
    assert len(value.operands) == 2


def can_generate_instance_with_two_references():
    _, program = prepare_program(
        """
            asm exit(id@imm: u64, code@imm: u8) { shl rax, code; mov rbx, id; }
            fn main() noreturn { exit(0x1234, 0x42); }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    instances = semantic.indices.instance_by_callsite

    assert instances.size() == 1
    id, value = instances.peak()

    assert isinstance(id, CallSiteId)
    assert isinstance(value, Instance)

    # kept only non-immediate argument
    assert len(value.bindings) == 0

    # rewritten two operands
    assert len(value.operands) == 2


def can_generate_instance_even_when_immediate_is_not_used():
    _, program = prepare_program(
        """
            asm exit(code@imm: u8) { syscall; }
            fn main() noreturn { exit(0x42); }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    instances = semantic.indices.instance_by_callsite

    assert instances.size() == 1


def can_rewrite_register_bound_slot_to_register():
    _, program = prepare_program(
        """
            asm foo(code@rax: u64) noreturn { mov code, 0x01; }
            fn main() noreturn { foo(0x42); }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    instances = semantic.indices.instance_by_callsite

    assert instances.size() == 1
    _, value = instances.peak()

    assert isinstance(value, Instance)

    # kept register-bound argument
    assert len(value.bindings) == 1

    # register-bound slot should be rewritten to register
    assert len(value.operands) == 1

    id, operand = next(iter(value.operands.items()))
    reference = semantic.basic.operands.get(id)

    assert reference.kind == b"reference"
    assert operand.kind == b"register"

    assert isinstance(operand.target, Register)
    assert operand.target.name == b"rax"
