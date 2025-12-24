from dataclasses import dataclass
from typing import Dict, List

from i13c import ast
from i13c.sem.core import Bidirectional, OneToMany, OneToOne
from i13c.sem.graph import (
    ArgumentId,
    CallId,
    FunctionId,
    Graph,
    ParameterId,
    StatementId,
)


@dataclass(kw_only=True)
class Type:
    name: bytes


@dataclass(kw_only=True)
class Register:
    name: bytes


@dataclass(kw_only=True)
class Analysis:
    is_terminal: OneToOne[FunctionId, bool]
    function_exits: OneToMany[FunctionId, StatementId]
    argument_types: OneToMany[ArgumentId, Type]
    parameter_types: OneToOne[ParameterId, Type]


def build_analysis(graph: Graph) -> Analysis:
    is_terminal = analysis_collect_is_terminal(graph.nodes.functions)

    function_exits = analysis_collect_function_exits(
        graph.nodes.functions, graph.nodes.statements
    )

    parameter_types = analysis_collect_parameter_types(graph.nodes.parameters)

    argument_types = analysis_collect_argument_types(
        graph.nodes.arguments,
        graph.edges.call_targets,
        graph.edges.call_arguments,
        graph.edges.function_parameters,
        parameter_types,
    )

    return Analysis(
        is_terminal=is_terminal,
        function_exits=function_exits,
        parameter_types=parameter_types,
        argument_types=argument_types,
    )


def analysis_collect_is_terminal(
    functions: Bidirectional[ast.Function, FunctionId],
) -> OneToOne[FunctionId, bool]:
    is_terminal: Dict[FunctionId, bool] = {}

    for fid, function in functions.items():
        is_terminal[fid] = function.terminal

    return OneToOne(map=is_terminal)


def analysis_collect_function_exits(
    functions: Bidirectional[ast.Function, FunctionId],
    statements: Bidirectional[ast.Statement, StatementId],
) -> OneToMany[FunctionId, StatementId]:
    function_exits: Dict[FunctionId, List[StatementId]] = {}

    for fid, function in functions.items():
        if isinstance(function, ast.RegFunction):
            if len(function.statements) > 0:
                function_exits[fid] = [statements.get_by_node(function.statements[-1])]

    return OneToMany(map=function_exits)


def analysis_collect_parameter_types(
    parameters: Bidirectional[ast.Parameter, ParameterId],
) -> OneToOne[ParameterId, Type]:
    parameter_types: Dict[ParameterId, Type] = {}

    for pid, parameter in parameters.items():
        parameter_types[pid] = Type(name=parameter.type.name)

    return OneToOne(map=parameter_types)


def analysis_collect_argument_types(
    arguments: Bidirectional[ast.Argument, ArgumentId],
    call_targets: OneToMany[CallId, FunctionId],
    call_arguments: OneToMany[CallId, ArgumentId],
    function_parameters: OneToMany[FunctionId, ParameterId],
    parameter_types: OneToOne[ParameterId, Type],
) -> OneToMany[ArgumentId, Type]:
    argument_types: Dict[ArgumentId, List[Type]] = {}

    def fits(value: int, typ: Type) -> bool:
        match typ.name:
            case b"u8":
                return 0 <= value <= 0xFF
            case b"u16":
                return 0 <= value <= 0xFFFF
            case b"u32":
                return 0 <= value <= 0xFFFFFFFF
            case b"u64":
                return 0 <= value <= 0xFFFFFFFFFFFFFFFF
            case _:
                return False

    for cid, fids in call_targets.items():
        aids = call_arguments.get(cid)

        for fid in fids:
            pids = function_parameters.get(fid)

            if len(aids) != len(pids):
                continue

            for aid, pid in zip(aids, pids):
                if ptype := parameter_types.find_by_id(pid):
                    if argument := arguments.find_by_id(aid):
                        if fits(argument.value, ptype):
                            argument_types.setdefault(aid, []).append(ptype)

    return OneToMany(map=argument_types)
