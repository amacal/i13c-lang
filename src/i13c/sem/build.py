from typing import Dict, List

from i13c import ast
from i13c.sem import rel


def build_semantic(program: ast.Program) -> rel.Relationships:
    functions = collect_functions(program)
    instructions = collect_instructions(functions)
    statements = collect_statements(functions)

    nodes = rel.Nodes(
        functions=functions,
        instructions=instructions,
        statements=statements,
        parameters=collect_parameters(functions),
        literals=collect_literals(functions),
        calls=collect_calls(functions),
    )

    edges = rel.Edges(
        function_parameters=collect_function_parameters(nodes),
        parameter_bindings=collect_parameter_bindings(nodes),
        function_clobbers=collect_function_clobbers(nodes),
        call_targets=collect_call_targets(nodes),
        statement_calls=collect_statement_calls(nodes),
    )

    analysis = rel.Analysis(
        is_terminal=collect_is_terminal(nodes, edges),
        function_exits=collect_function_exits(nodes, edges),
    )

    return rel.Relationships(nodes=nodes, edges=edges, analysis=analysis)


def collect_functions(
    program: ast.Program,
) -> rel.Bidirectional[ast.Function, rel.FunctionId]:
    id_to_node: Dict[rel.FunctionId, ast.Function] = {}
    node_to_id: Dict[ast.Function, rel.FunctionId] = {}
    name_to_node: Dict[bytes, rel.FunctionId] = {}

    # counter
    next = 1

    for function in program.functions:
        node_to_id[function] = rel.FunctionId(value=next)
        id_to_node[rel.FunctionId(value=next)] = function
        name_to_node[function.name] = node_to_id[function]

        # increment
        next += 1

    return rel.Bidirectional(
        node_to_id=node_to_id,
        id_to_node=id_to_node,
        attr_to_id={"name": name_to_node},
    )


def collect_instructions(
    functions: rel.Bidirectional[ast.Function, rel.FunctionId],
) -> rel.Bidirectional[ast.Instruction, rel.InstructionId]:
    id_to_node: Dict[rel.InstructionId, ast.Instruction] = {}
    node_to_id: Dict[ast.Instruction, rel.InstructionId] = {}

    # counter
    next = 1

    for function in functions.values():
        if isinstance(function, ast.AsmFunction):
            for instruction in function.instructions:
                node_to_id[instruction] = rel.InstructionId(value=next)
                id_to_node[rel.InstructionId(value=next)] = instruction

                # increment
                next += 1

    return rel.Bidirectional(
        node_to_id=node_to_id,
        id_to_node=id_to_node,
        attr_to_id={},
    )


def collect_statements(
    functions: rel.Bidirectional[ast.Function, rel.FunctionId],
) -> rel.Bidirectional[ast.Statement, rel.StatementId]:
    id_to_node: Dict[rel.StatementId, ast.Statement] = {}
    node_to_id: Dict[ast.Statement, rel.StatementId] = {}

    # counter
    next = 1

    for function in functions.values():
        if isinstance(function, ast.RegFunction):
            for statement in function.statements:
                node_to_id[statement] = rel.StatementId(value=next)
                id_to_node[rel.StatementId(value=next)] = statement

                # increment
                next += 1

    return rel.Bidirectional(
        node_to_id=node_to_id,
        id_to_node=id_to_node,
        attr_to_id={},
    )


def collect_parameters(
    functions: rel.Bidirectional[ast.Function, rel.FunctionId],
) -> rel.Bidirectional[ast.Parameter, rel.ParameterId]:
    id_to_node: Dict[rel.ParameterId, ast.Parameter] = {}
    node_to_id: Dict[ast.Parameter, rel.ParameterId] = {}

    # counter
    next = 1

    for function in functions.values():
        for parameter in function.parameters:
            node_to_id[parameter] = rel.ParameterId(value=next)
            id_to_node[rel.ParameterId(value=next)] = parameter

            # increment
            next += 1

    return rel.Bidirectional(
        node_to_id=node_to_id,
        id_to_node=id_to_node,
        attr_to_id={},
    )


def collect_literals(
    functions: rel.Bidirectional[ast.Function, rel.FunctionId],
) -> rel.Bidirectional[ast.Literal, rel.LiteralId]:
    id_to_node: Dict[rel.LiteralId, ast.Literal] = {}
    node_to_id: Dict[ast.Literal, rel.LiteralId] = {}

    # counter
    next = 1

    for function in functions.values():
        if isinstance(function, ast.RegFunction):
            for statement in function.statements:
                for argument in statement.arguments:
                    node_to_id[argument] = rel.LiteralId(value=next)
                    id_to_node[rel.LiteralId(value=next)] = argument

                    # increment
                    next += 1

    return rel.Bidirectional(
        node_to_id=node_to_id,
        id_to_node=id_to_node,
        attr_to_id={},
    )


def collect_calls(
    functions: rel.Bidirectional[ast.Function, rel.FunctionId],
) -> rel.Bidirectional[ast.CallStatement, rel.CallId]:
    id_to_node: Dict[rel.CallId, ast.CallStatement] = {}
    node_to_id: Dict[ast.CallStatement, rel.CallId] = {}

    # counter
    next = 1

    for function in functions.values():
        if isinstance(function, ast.RegFunction):
            for statement in function.statements:
                node_to_id[statement] = rel.CallId(value=next)
                id_to_node[rel.CallId(value=next)] = statement

                # increment
                next += 1

    return rel.Bidirectional(
        node_to_id=node_to_id,
        id_to_node=id_to_node,
        attr_to_id={},
    )


def collect_function_parameters(
    nodes: rel.Nodes,
) -> rel.OneToMany[rel.FunctionId, rel.ParameterId]:
    function_parameters: Dict[rel.FunctionId, List[rel.ParameterId]] = {}

    for fid, function in nodes.functions.items():
        function_parameters[fid] = [
            nodes.parameters.get_by_node(parameter) for parameter in function.parameters
        ]

    return rel.OneToMany(map=function_parameters)


def collect_parameter_bindings(
    nodes: rel.Nodes,
) -> rel.OneToOne[rel.ParameterId, ast.Register]:
    parameter_bindings: Dict[rel.ParameterId, ast.Register] = {}

    for function in nodes.functions.values():
        if isinstance(function, ast.AsmFunction):
            for parameter in function.parameters:
                parameter_bindings[nodes.parameters.get_by_node(parameter)] = (
                    parameter.bind
                )

    return rel.OneToOne(map=parameter_bindings)


def collect_function_clobbers(
    nodes: rel.Nodes,
) -> rel.OneToMany[rel.FunctionId, ast.Register]:
    function_clobbers: Dict[rel.FunctionId, List[ast.Register]] = {}

    for function in nodes.functions.values():
        if isinstance(function, ast.AsmFunction):
            function_clobbers[nodes.functions.get_by_node(function)] = function.clobbers

    return rel.OneToMany(map=function_clobbers)


def collect_call_targets(
    nodes: rel.Nodes,
) -> rel.OneToOne[rel.CallId, rel.FunctionId]:
    call_targets: Dict[rel.CallId, rel.FunctionId] = {}

    for statement in nodes.statements.values():
        if target := nodes.functions.find_by_attr("name", statement.name):
            call_targets[nodes.calls.get_by_node(statement)] = target

    return rel.OneToOne(map=call_targets)


def collect_statement_calls(
    nodes: rel.Nodes,
) -> rel.OneToOne[rel.StatementId, rel.CallId]:
    statement_calls: Dict[rel.StatementId, rel.CallId] = {}

    for sid, statement in nodes.statements.items():
        if cid := nodes.calls.find_by_node(statement):
            statement_calls[sid] = cid

    return rel.OneToOne(map=statement_calls)


def collect_is_terminal(
    nodes: rel.Nodes,
    edges: rel.Edges,
) -> rel.OneToOne[rel.FunctionId, bool]:
    is_terminal: Dict[rel.FunctionId, bool] = {}

    for fid, function in nodes.functions.items():
        is_terminal[fid] = function.terminal

    return rel.OneToOne(map=is_terminal)


def collect_function_exits(
    nodes: rel.Nodes,
    edges: rel.Edges,
) -> rel.OneToMany[rel.FunctionId, rel.StatementId]:
    function_exits: Dict[rel.FunctionId, List[rel.StatementId]] = {}

    for fid, function in nodes.functions.items():
        exits: List[rel.StatementId] = []

        if isinstance(function, ast.RegFunction):
            if len(function.statements) > 0:
                exits.append(nodes.statements.get_by_node(function.statements[-1]))

        function_exits[fid] = exits

    return rel.OneToMany(map=function_exits)
