from dataclasses import dataclass
from typing import Dict, List

from i13c import ast
from i13c.sem.core import Bidirectional, OneToMany, OneToOne


@dataclass(kw_only=True, frozen=True)
class FunctionId:
    value: int


@dataclass(kw_only=True, frozen=True)
class InstructionId:
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
    instructions: Bidirectional[ast.Instruction, InstructionId]
    statements: Bidirectional[ast.Statement, StatementId]
    parameters: Bidirectional[ast.Parameter, ParameterId]
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
    function_clobbers: OneToMany[FunctionId, RegisterId]
    parameter_bindings: OneToOne[ParameterId, RegisterId]
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
    instructions = node_collect_instructions(functions)
    statements = node_collect_statements(functions)
    parameters = node_collect_parameters(functions)
    calls = node_collect_calls(statements)
    arguments = node_collect_arguments(calls)
    literals = node_collect_literals(arguments)
    registers = node_collect_registers(functions, parameters)

    # indices
    functions_by_name = index_collect_functions_by_name(functions)

    # edges
    function_parameters = edges_collect_function_parameters(functions, parameters)
    function_clobbers = edge_collect_function_clobbers(functions, registers)
    parameter_bindings = edge_collect_parameter_bindings(parameters, registers)
    call_targets = edge_collect_call_targets(calls, functions_by_name)
    call_arguments = edge_collect_call_arguments(calls, arguments)
    statement_calls = edge_collect_statement_calls(statements, calls)

    return Graph(
        nodes=Nodes(
            functions=functions,
            instructions=instructions,
            statements=statements,
            parameters=parameters,
            calls=calls,
            arguments=arguments,
            literals=literals,
            registers=registers,
        ),
        edges=Edges(
            function_parameters=function_parameters,
            function_clobbers=function_clobbers,
            parameter_bindings=parameter_bindings,
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


def node_collect_instructions(
    functions: Bidirectional[ast.Function, FunctionId],
) -> Bidirectional[ast.Instruction, InstructionId]:
    id_to_node: Dict[InstructionId, ast.Instruction] = {}
    node_to_id: Dict[ast.Instruction, InstructionId] = {}

    # counter
    next = 1

    for function in functions.values():
        if isinstance(function, ast.AsmFunction):
            for instruction in function.instructions:
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
        if isinstance(function, ast.RegFunction):
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
    functions: Bidirectional[ast.Function, FunctionId],
    parameters: Bidirectional[ast.Parameter, ParameterId],
) -> Bidirectional[ast.Register, RegisterId]:
    id_to_node: Dict[RegisterId, ast.Register] = {}
    node_to_id: Dict[ast.Register, RegisterId] = {}

    # counter
    next = 1

    for function in functions.values():
        if isinstance(function, ast.AsmFunction):
            for register in function.clobbers:
                node_to_id[register] = RegisterId(value=next)
                id_to_node[RegisterId(value=next)] = register

                # increment
                next += 1

    for parameter in parameters.values():
        if isinstance(parameter, ast.AsmParameter):
            node_to_id[parameter.bind] = RegisterId(value=next)
            id_to_node[RegisterId(value=next)] = parameter.bind

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
        if function.name not in functions_by_name:
            functions_by_name[function.name] = []
        functions_by_name[function.name].append(fid)

    return OneToMany(map=functions_by_name)


def edges_collect_function_parameters(
    functions: Bidirectional[ast.Function, FunctionId],
    parameters: Bidirectional[ast.Parameter, ParameterId],
) -> OneToMany[FunctionId, ParameterId]:
    function_parameters: Dict[FunctionId, List[ParameterId]] = {}

    for fid, function in functions.items():
        function_parameters[fid] = parameters.get_by_nodes(function.parameters)

    return OneToMany(map=function_parameters)


def edge_collect_parameter_bindings(
    parameters: Bidirectional[ast.Parameter, ParameterId],
    registers: Bidirectional[ast.Register, RegisterId],
) -> OneToOne[ParameterId, RegisterId]:
    parameter_bindings: Dict[ParameterId, RegisterId] = {}

    for pid, parameter in parameters.items():
        if isinstance(parameter, ast.AsmParameter):
            parameter_bindings[pid] = registers.get_by_node(parameter.bind)

    return OneToOne(map=parameter_bindings)


def edge_collect_function_clobbers(
    functions: Bidirectional[ast.Function, FunctionId],
    registers: Bidirectional[ast.Register, RegisterId],
) -> OneToMany[FunctionId, RegisterId]:
    function_clobbers: Dict[FunctionId, List[RegisterId]] = {}

    for fid, function in functions.items():
        if isinstance(function, ast.AsmFunction):
            function_clobbers[fid] = registers.get_by_nodes(function.clobbers)

    return OneToMany(map=function_clobbers)


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
