from dataclasses import dataclass
from typing import Dict, List

from i13c import ast
from i13c.sem.core import Bidirectional, OneToMany, OneToOne


@dataclass(kw_only=True, frozen=True)
class FunctionId:
    value: int


@dataclass(kw_only=True, frozen=True)
class SnippetId:
    value: int


@dataclass(kw_only=True, frozen=True)
class InstructionId:
    value: int


@dataclass(kw_only=True, frozen=True)
class SlotId:
    value: int


@dataclass(kw_only=True, frozen=True)
class ParameterId:
    value: int


@dataclass(kw_only=True, frozen=True)
class LiteralId:
    value: int


@dataclass(kw_only=True, frozen=True)
class RegisterId:
    value: int


@dataclass(kw_only=True, frozen=True)
class CallId:
    value: int


@dataclass(kw_only=True, frozen=True)
class StatementId:
    value: int


@dataclass(kw_only=True, frozen=True)
class ArgumentId:
    value: int


@dataclass(kw_only=True)
class Nodes:
    functions: Bidirectional[ast.Function, FunctionId]
    snippets: Bidirectional[ast.Snippet, SnippetId]
    instructions: Bidirectional[ast.Instruction, InstructionId]
    statements: Bidirectional[ast.Statement, StatementId]
    parameters: Bidirectional[ast.Parameter, ParameterId]
    slots: Bidirectional[ast.Slot, SlotId]
    arguments: Bidirectional[ast.Argument, ArgumentId]
    literals: Bidirectional[ast.Literal, LiteralId]
    registers: Bidirectional[ast.Register, RegisterId]
    calls: Bidirectional[ast.CallStatement, CallId]


@dataclass(kw_only=True)
class Indices:
    functions_by_name: OneToMany[bytes, FunctionId]


@dataclass(kw_only=True)
class Edges:
    function_parameters: OneToMany[FunctionId, ParameterId]
    snippet_clobbers: OneToMany[SnippetId, RegisterId]
    snippet_slots: OneToMany[SnippetId, SlotId]
    slot_bindings: OneToOne[SlotId, RegisterId]
    call_targets: OneToMany[CallId, FunctionId]
    call_arguments: OneToMany[CallId, ArgumentId]
    statement_calls: OneToOne[StatementId, CallId]


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
    call_targets = edge_collect_call_targets(calls, functions_by_name)
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
            call_targets=call_targets,
            call_arguments=call_arguments,
            statement_calls=statement_calls,
        ),
        indices=Indices(
            functions_by_name=functions_by_name,
        ),
    )


def node_collect_functions(
    program: ast.Program,
) -> Bidirectional[ast.Function, FunctionId]:
    id_to_node: Dict[FunctionId, ast.Function] = {}
    node_to_id: Dict[ast.Function, FunctionId] = {}
    name_to_node: Dict[bytes, FunctionId] = {}

    # counter
    next = 1

    for function in program.functions:
        node_to_id[function] = FunctionId(value=next)
        id_to_node[FunctionId(value=next)] = function
        name_to_node[function.name] = node_to_id[function]

        # increment
        next += 1

    return Bidirectional(
        node_to_id=node_to_id,
        id_to_node=id_to_node,
    )


def node_collect_snippets(
    program: ast.Program,
) -> Bidirectional[ast.Snippet, SnippetId]:
    id_to_node: Dict[SnippetId, ast.Snippet] = {}
    node_to_id: Dict[ast.Snippet, SnippetId] = {}

    # counter
    next = 1

    for snippet in program.snippets:
        node_to_id[snippet] = SnippetId(value=next)
        id_to_node[SnippetId(value=next)] = snippet

        # increment
        next += 1

    return Bidirectional(
        node_to_id=node_to_id,
        id_to_node=id_to_node,
    )


def node_collect_instructions(
    snippets: Bidirectional[ast.Snippet, SnippetId],
) -> Bidirectional[ast.Instruction, InstructionId]:
    id_to_node: Dict[InstructionId, ast.Instruction] = {}
    node_to_id: Dict[ast.Instruction, InstructionId] = {}

    # counter
    next = 1

    for snippet in snippets.values():
        for instruction in snippet.instructions:
            node_to_id[instruction] = InstructionId(value=next)
            id_to_node[InstructionId(value=next)] = instruction

            # increment
            next += 1

    return Bidirectional(
        node_to_id=node_to_id,
        id_to_node=id_to_node,
    )


def node_collect_statements(
    functions: Bidirectional[ast.Function, FunctionId],
) -> Bidirectional[ast.Statement, StatementId]:
    id_to_node: Dict[StatementId, ast.Statement] = {}
    node_to_id: Dict[ast.Statement, StatementId] = {}

    # counter
    next = 1

    for function in functions.values():
        for statement in function.statements:
            node_to_id[statement] = StatementId(value=next)
            id_to_node[StatementId(value=next)] = statement

            # increment
            next += 1

    return Bidirectional(
        node_to_id=node_to_id,
        id_to_node=id_to_node,
    )


def node_collect_parameters(
    functions: Bidirectional[ast.Function, FunctionId],
) -> Bidirectional[ast.Parameter, ParameterId]:
    id_to_node: Dict[ParameterId, ast.Parameter] = {}
    node_to_id: Dict[ast.Parameter, ParameterId] = {}

    # counter
    next = 1

    for function in functions.values():
        for parameter in function.parameters:
            node_to_id[parameter] = ParameterId(value=next)
            id_to_node[ParameterId(value=next)] = parameter

            # increment
            next += 1

    return Bidirectional(
        node_to_id=node_to_id,
        id_to_node=id_to_node,
    )


def node_collect_slots(
    snippets: Bidirectional[ast.Snippet, SnippetId],
) -> Bidirectional[ast.Slot, SlotId]:
    id_to_node: Dict[SlotId, ast.Slot] = {}
    node_to_id: Dict[ast.Slot, SlotId] = {}

    # counter
    next = 1

    for snippet in snippets.values():
        for slot in snippet.slots:
            node_to_id[slot] = SlotId(value=next)
            id_to_node[SlotId(value=next)] = slot

            # increment
            next += 1

    return Bidirectional(
        node_to_id=node_to_id,
        id_to_node=id_to_node,
    )


def node_collect_calls(
    statements: Bidirectional[ast.Statement, StatementId],
) -> Bidirectional[ast.CallStatement, CallId]:
    id_to_node: Dict[CallId, ast.CallStatement] = {}
    node_to_id: Dict[ast.CallStatement, CallId] = {}

    # counter
    next = 1

    for statement in statements.values():
        node_to_id[statement] = CallId(value=next)
        id_to_node[CallId(value=next)] = statement

        # increment
        next += 1

    return Bidirectional(
        node_to_id=node_to_id,
        id_to_node=id_to_node,
    )


def node_collect_arguments(
    calls: Bidirectional[ast.CallStatement, CallId],
) -> Bidirectional[ast.Argument, ArgumentId]:
    id_to_node: Dict[ArgumentId, ast.Argument] = {}
    node_to_id: Dict[ast.Argument, ArgumentId] = {}

    # counter
    next = 1

    for call in calls.values():
        for argument in call.arguments:
            node_to_id[argument] = ArgumentId(value=next)
            id_to_node[ArgumentId(value=next)] = argument

            # increment
            next += 1

    return Bidirectional(
        node_to_id=node_to_id,
        id_to_node=id_to_node,
    )


def node_collect_literals(
    arguments: Bidirectional[ast.Argument, ArgumentId],
) -> Bidirectional[ast.Literal, LiteralId]:
    id_to_node: Dict[LiteralId, ast.Literal] = {}
    node_to_id: Dict[ast.Literal, LiteralId] = {}

    # counter
    next = 1

    for argument in arguments.values():
        node_to_id[argument] = LiteralId(value=next)
        id_to_node[LiteralId(value=next)] = argument

        # increment
        next += 1

    return Bidirectional(
        node_to_id=node_to_id,
        id_to_node=id_to_node,
    )


def node_collect_registers(
    snippets: Bidirectional[ast.Snippet, SnippetId],
    slots: Bidirectional[ast.Slot, SlotId],
) -> Bidirectional[ast.Register, RegisterId]:
    id_to_node: Dict[RegisterId, ast.Register] = {}
    node_to_id: Dict[ast.Register, RegisterId] = {}

    # counter
    next = 1

    for snippet in snippets.values():
        for register in snippet.clobbers:
            node_to_id[register] = RegisterId(value=next)
            id_to_node[RegisterId(value=next)] = register

            # increment
            next += 1

    for slot in slots.values():
        node_to_id[slot.bind] = RegisterId(value=next)
        id_to_node[RegisterId(value=next)] = slot.bind

        # increment
        next += 1

    return Bidirectional(
        node_to_id=node_to_id,
        id_to_node=id_to_node,
    )


def index_collect_functions_by_name(
    functions: Bidirectional[ast.Function, FunctionId],
) -> OneToMany[bytes, FunctionId]:
    functions_by_name: Dict[bytes, List[FunctionId]] = {}

    for fid, function in functions.items():
        functions_by_name.setdefault(function.name, []).append(fid)

    return OneToMany(map=functions_by_name)


def edges_collect_function_parameters(
    functions: Bidirectional[ast.Function, FunctionId],
    parameters: Bidirectional[ast.Parameter, ParameterId],
) -> OneToMany[FunctionId, ParameterId]:
    function_parameters: Dict[FunctionId, List[ParameterId]] = {}

    for fid, function in functions.items():
        function_parameters[fid] = parameters.get_by_nodes(function.parameters)

    return OneToMany(map=function_parameters)


def edge_collect_slot_bindings(
    slots: Bidirectional[ast.Slot, SlotId],
    registers: Bidirectional[ast.Register, RegisterId],
) -> OneToOne[SlotId, RegisterId]:
    out: Dict[SlotId, RegisterId] = {}

    for sid, slot in slots.items():
        out[sid] = registers.get_by_node(slot.bind)

    return OneToOne(map=out)


def edge_collect_snippet_clobbers(
    snippets: Bidirectional[ast.Snippet, SnippetId],
    registers: Bidirectional[ast.Register, RegisterId],
) -> OneToMany[SnippetId, RegisterId]:
    out: Dict[SnippetId, List[RegisterId]] = {}

    for sid, snippet in snippets.items():
        out[sid] = registers.get_by_nodes(snippet.clobbers)

    return OneToMany(map=out)


def edge_collect_snippet_slots(
    snippets: Bidirectional[ast.Snippet, SnippetId],
    slots: Bidirectional[ast.Slot, SlotId],
) -> OneToMany[SnippetId, SlotId]:
    out: Dict[SnippetId, List[SlotId]] = {}

    for sid, snippet in snippets.items():
        out[sid] = slots.get_by_nodes(snippet.slots)

    return OneToMany(map=out)


def edge_collect_call_targets(
    calls: Bidirectional[ast.CallStatement, CallId],
    functions_by_name: OneToMany[bytes, FunctionId],
) -> OneToMany[CallId, FunctionId]:
    call_targets: Dict[CallId, List[FunctionId]] = {}

    for cid, call in calls.items():
        if targets := functions_by_name.get(call.name):
            call_targets[cid] = targets

    return OneToMany(map=call_targets)


def edge_collect_call_arguments(
    calls: Bidirectional[ast.CallStatement, CallId],
    arguments: Bidirectional[ast.Argument, ArgumentId],
) -> OneToMany[CallId, ArgumentId]:
    call_arguments: Dict[CallId, List[ArgumentId]] = {}

    for cid, call in calls.items():
        if aids := arguments.get_by_nodes(call.arguments):
            call_arguments[cid] = aids

    return OneToMany(map=call_arguments)


def edge_collect_statement_calls(
    statements: Bidirectional[ast.Statement, StatementId],
    calls: Bidirectional[ast.CallStatement, CallId],
) -> OneToOne[StatementId, CallId]:
    statement_calls: Dict[StatementId, CallId] = {}

    for sid, statement in statements.items():
        if cid := calls.find_by_node(statement):
            statement_calls[sid] = cid

    return OneToOne(map=statement_calls)
