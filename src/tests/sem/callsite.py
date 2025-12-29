from i13c.sem import callsite, model, syntax
from tests.sem import prepare_program


def can_build_semantic_model_callsites():
    _, program = prepare_program(
        """
            fn main() noreturn { foo(0x42); }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    callsites = semantic.callsites

    assert len(callsites) == 1
    id, value = callsites.popitem()

    assert isinstance(id, callsite.CallSiteId)
    assert isinstance(value, callsite.CallSite)

    assert value.callee.name == b"foo"
    assert len(value.arguments) == 1

    argument = value.arguments[0]
    assert argument.kind == b"literal"

    assert isinstance(argument.target, callsite.LiteralId)
    lid = syntax.NodeId(value=argument.target.value)

    literal = graph.nodes.literals.get_by_id(lid)
    assert literal.value == 0x42
