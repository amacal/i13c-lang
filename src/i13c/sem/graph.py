from dataclasses import dataclass
from typing import Dict, List

from i13c import ast
from i13c.sem import ids
from i13c.sem.core import Bidirectional, OneToMany, OneToOne


@dataclass(kw_only=True)
class Nodes:
    functions: Bidirectional[ast.Function, ids.FunctionId]
    snippets: Bidirectional[ast.Snippet, ids.SnippetId]
    instructions: Bidirectional[ast.Instruction, ids.InstructionId]
    statements: Bidirectional[ast.Statement, ids.StatementId]
    parameters: Bidirectional[ast.Parameter, ids.ParameterId]
    slots: Bidirectional[ast.Slot, ids.SlotId]
    arguments: Bidirectional[ast.Argument, ids.ArgumentId]
    literals: Bidirectional[ast.Literal, ids.LiteralId]
    registers: Bidirectional[ast.Register, ids.RegisterId]
    calls: Bidirectional[ast.CallStatement, ids.CallId]


@dataclass(kw_only=True)
class Indices:
    functions_by_name: OneToMany[bytes, ids.FunctionId]


@dataclass(kw_only=True)
class Edges:
    function_parameters: OneToMany[ids.FunctionId, ids.ParameterId]
    snippet_clobbers: OneToMany[ids.SnippetId, ids.RegisterId]
    snippet_slots: OneToMany[ids.SnippetId, ids.SlotId]
    slot_bindings: OneToOne[ids.SlotId, ids.RegisterId]
    call_arguments: OneToMany[ids.CallId, ids.ArgumentId]
    statement_calls: OneToOne[ids.StatementId, ids.CallId]


@dataclass(kw_only=True)
class Graph:
    nodes: Nodes
    edges: Edges
    indices: Indices


def build_graph(program: ast.Program) -> Graph:
    # nodes
    functions = node_collect_functions(program)
    snippets = node_collect_snippets(program)

    instructions = node_collect_instructions(snippets)
    statements = node_collect_statements(functions)

    parameters = node_collect_parameters(functions)
    slots = node_collect_slots(snippets)

    calls = node_collect_calls(statements)
    arguments = node_collect_arguments(calls)
    literals = node_collect_literals(arguments)
    registers = node_collect_registers(snippets, slots)

    # indices
    functions_by_name = index_collect_functions_by_name(functions)

    # edges
    function_parameters = edges_collect_function_parameters(functions, parameters)
    snippet_clobbers = edge_collect_snippet_clobbers(snippets, registers)
    snippet_slots = edge_collect_snippet_slots(snippets, slots)
    slot_bindings = edge_collect_slot_bindings(slots, registers)
    call_arguments = edge_collect_call_arguments(calls, arguments)
    statement_calls = edge_collect_statement_calls(statements, calls)

    return Graph(
        nodes=Nodes(
            functions=functions,
            snippets=snippets,
            instructions=instructions,
            statements=statements,
            parameters=parameters,
            slots=slots,
            calls=calls,
            arguments=arguments,
            literals=literals,
            registers=registers,
        ),
        edges=Edges(
            function_parameters=function_parameters,
            snippet_clobbers=snippet_clobbers,
            snippet_slots=snippet_slots,
            slot_bindings=slot_bindings,
            call_arguments=call_arguments,
            statement_calls=statement_calls,
        ),
        indices=Indices(
            functions_by_name=functions_by_name,
        ),
    )


def node_collect_functions(
    program: ast.Program,
) -> Bidirectional[ast.Function, ids.FunctionId]:
    id_to_node: Dict[ids.FunctionId, ast.Function] = {}
    node_to_id: Dict[ast.Function, ids.FunctionId] = {}
    name_to_node: Dict[bytes, ids.FunctionId] = {}

    # counter
    next = 1

    for function in program.functions:
        node_to_id[function] = ids.FunctionId(value=next)
        id_to_node[ids.FunctionId(value=next)] = function
        name_to_node[function.name] = node_to_id[function]

        # increment
        next += 1

    return Bidirectional(
        node_to_id=node_to_id,
        id_to_node=id_to_node,
    )


def node_collect_snippets(
    program: ast.Program,
) -> Bidirectional[ast.Snippet, ids.SnippetId]:
    id_to_node: Dict[ids.SnippetId, ast.Snippet] = {}
    node_to_id: Dict[ast.Snippet, ids.SnippetId] = {}

    # counter
    next = 1

    for snippet in program.snippets:
        node_to_id[snippet] = ids.SnippetId(value=next)
        id_to_node[ids.SnippetId(value=next)] = snippet

        # increment
        next += 1

    return Bidirectional(
        node_to_id=node_to_id,
        id_to_node=id_to_node,
    )


def node_collect_instructions(
    snippets: Bidirectional[ast.Snippet, ids.SnippetId],
) -> Bidirectional[ast.Instruction, ids.InstructionId]:
    id_to_node: Dict[ids.InstructionId, ast.Instruction] = {}
    node_to_id: Dict[ast.Instruction, ids.InstructionId] = {}

    # counter
    next = 1

    for snippet in snippets.values():
        for instruction in snippet.instructions:
            node_to_id[instruction] = ids.InstructionId(value=next)
            id_to_node[ids.InstructionId(value=next)] = instruction

            # increment
            next += 1

    return Bidirectional(
        node_to_id=node_to_id,
        id_to_node=id_to_node,
    )


def node_collect_statements(
    functions: Bidirectional[ast.Function, ids.FunctionId],
) -> Bidirectional[ast.Statement, ids.StatementId]:
    id_to_node: Dict[ids.StatementId, ast.Statement] = {}
    node_to_id: Dict[ast.Statement, ids.StatementId] = {}

    # counter
    next = 1

    for function in functions.values():
        for statement in function.statements:
            node_to_id[statement] = ids.StatementId(value=next)
            id_to_node[ids.StatementId(value=next)] = statement

            # increment
            next += 1

    return Bidirectional(
        node_to_id=node_to_id,
        id_to_node=id_to_node,
    )


def node_collect_parameters(
    functions: Bidirectional[ast.Function, ids.FunctionId],
) -> Bidirectional[ast.Parameter, ids.ParameterId]:
    id_to_node: Dict[ids.ParameterId, ast.Parameter] = {}
    node_to_id: Dict[ast.Parameter, ids.ParameterId] = {}

    # counter
    next = 1

    for function in functions.values():
        for parameter in function.parameters:
            node_to_id[parameter] = ids.ParameterId(value=next)
            id_to_node[ids.ParameterId(value=next)] = parameter

            # increment
            next += 1

    return Bidirectional(
        node_to_id=node_to_id,
        id_to_node=id_to_node,
    )


def node_collect_slots(
    snippets: Bidirectional[ast.Snippet, ids.SnippetId],
) -> Bidirectional[ast.Slot, ids.SlotId]:
    id_to_node: Dict[ids.SlotId, ast.Slot] = {}
    node_to_id: Dict[ast.Slot, ids.SlotId] = {}

    # counter
    next = 1

    for snippet in snippets.values():
        for slot in snippet.slots:
            node_to_id[slot] = ids.SlotId(value=next)
            id_to_node[ids.SlotId(value=next)] = slot

            # increment
            next += 1

    return Bidirectional(
        node_to_id=node_to_id,
        id_to_node=id_to_node,
    )


def node_collect_calls(
    statements: Bidirectional[ast.Statement, ids.StatementId],
) -> Bidirectional[ast.CallStatement, ids.CallId]:
    id_to_node: Dict[ids.CallId, ast.CallStatement] = {}
    node_to_id: Dict[ast.CallStatement, ids.CallId] = {}

    # counter
    next = 1

    for statement in statements.values():
        node_to_id[statement] = ids.CallId(value=next)
        id_to_node[ids.CallId(value=next)] = statement

        # increment
        next += 1

    return Bidirectional(
        node_to_id=node_to_id,
        id_to_node=id_to_node,
    )


def node_collect_arguments(
    calls: Bidirectional[ast.CallStatement, ids.CallId],
) -> Bidirectional[ast.Argument, ids.ArgumentId]:
    id_to_node: Dict[ids.ArgumentId, ast.Argument] = {}
    node_to_id: Dict[ast.Argument, ids.ArgumentId] = {}

    # counter
    next = 1

    for call in calls.values():
        for argument in call.arguments:
            node_to_id[argument] = ids.ArgumentId(value=next)
            id_to_node[ids.ArgumentId(value=next)] = argument

            # increment
            next += 1

    return Bidirectional(
        node_to_id=node_to_id,
        id_to_node=id_to_node,
    )


def node_collect_literals(
    arguments: Bidirectional[ast.Argument, ids.ArgumentId],
) -> Bidirectional[ast.Literal, ids.LiteralId]:
    id_to_node: Dict[ids.LiteralId, ast.Literal] = {}
    node_to_id: Dict[ast.Literal, ids.LiteralId] = {}

    # counter
    next = 1

    for argument in arguments.values():
        node_to_id[argument] = ids.LiteralId(value=next)
        id_to_node[ids.LiteralId(value=next)] = argument

        # increment
        next += 1

    return Bidirectional(
        node_to_id=node_to_id,
        id_to_node=id_to_node,
    )


def node_collect_registers(
    snippets: Bidirectional[ast.Snippet, ids.SnippetId],
    slots: Bidirectional[ast.Slot, ids.SlotId],
) -> Bidirectional[ast.Register, ids.RegisterId]:
    id_to_node: Dict[ids.RegisterId, ast.Register] = {}
    node_to_id: Dict[ast.Register, ids.RegisterId] = {}

    # counter
    next = 1

    for snippet in snippets.values():
        for register in snippet.clobbers:
            node_to_id[register] = ids.RegisterId(value=next)
            id_to_node[ids.RegisterId(value=next)] = register

            # increment
            next += 1

    for slot in slots.values():
        node_to_id[slot.bind] = ids.RegisterId(value=next)
        id_to_node[ids.RegisterId(value=next)] = slot.bind

        # increment
        next += 1

    return Bidirectional(
        node_to_id=node_to_id,
        id_to_node=id_to_node,
    )


def index_collect_functions_by_name(
    functions: Bidirectional[ast.Function, ids.FunctionId],
) -> OneToMany[bytes, ids.FunctionId]:
    functions_by_name: Dict[bytes, List[ids.FunctionId]] = {}

    for fid, function in functions.items():
        functions_by_name.setdefault(function.name, []).append(fid)

    return OneToMany(map=functions_by_name)


def edges_collect_function_parameters(
    functions: Bidirectional[ast.Function, ids.FunctionId],
    parameters: Bidirectional[ast.Parameter, ids.ParameterId],
) -> OneToMany[ids.FunctionId, ids.ParameterId]:
    function_parameters: Dict[ids.FunctionId, List[ids.ParameterId]] = {}

    for fid, function in functions.items():
        function_parameters[fid] = parameters.get_by_nodes(function.parameters)

    return OneToMany(map=function_parameters)


def edge_collect_slot_bindings(
    slots: Bidirectional[ast.Slot, ids.SlotId],
    registers: Bidirectional[ast.Register, ids.RegisterId],
) -> OneToOne[ids.SlotId, ids.RegisterId]:
    out: Dict[ids.SlotId, ids.RegisterId] = {}

    for sid, slot in slots.items():
        out[sid] = registers.get_by_node(slot.bind)

    return OneToOne(map=out)


def edge_collect_snippet_clobbers(
    snippets: Bidirectional[ast.Snippet, ids.SnippetId],
    registers: Bidirectional[ast.Register, ids.RegisterId],
) -> OneToMany[ids.SnippetId, ids.RegisterId]:
    out: Dict[ids.SnippetId, List[ids.RegisterId]] = {}

    for sid, snippet in snippets.items():
        out[sid] = registers.get_by_nodes(snippet.clobbers)

    return OneToMany(map=out)


def edge_collect_snippet_slots(
    snippets: Bidirectional[ast.Snippet, ids.SnippetId],
    slots: Bidirectional[ast.Slot, ids.SlotId],
) -> OneToMany[ids.SnippetId, ids.SlotId]:
    out: Dict[ids.SnippetId, List[ids.SlotId]] = {}

    for sid, snippet in snippets.items():
        out[sid] = slots.get_by_nodes(snippet.slots)

    return OneToMany(map=out)


def edge_collect_call_arguments(
    calls: Bidirectional[ast.CallStatement, ids.CallId],
    arguments: Bidirectional[ast.Argument, ids.ArgumentId],
) -> OneToMany[ids.CallId, ids.ArgumentId]:
    call_arguments: Dict[ids.CallId, List[ids.ArgumentId]] = {}

    for cid, call in calls.items():
        if aids := arguments.get_by_nodes(call.arguments):
            call_arguments[cid] = aids

    return OneToMany(map=call_arguments)


def edge_collect_statement_calls(
    statements: Bidirectional[ast.Statement, ids.StatementId],
    calls: Bidirectional[ast.CallStatement, ids.CallId],
) -> OneToOne[ids.StatementId, ids.CallId]:
    statement_calls: Dict[ids.StatementId, ids.CallId] = {}

    for sid, statement in statements.items():
        if cid := calls.find_by_node(statement):
            statement_calls[sid] = cid

    return OneToOne(map=statement_calls)
