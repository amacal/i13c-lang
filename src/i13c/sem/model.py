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
from i13c.sem.types import CallSite, SlotBinding, Type


@dataclass
class Resolver:
    by_name: OneToMany[CallId, FunctionId]
    by_arity: OneToMany[CallId, FunctionId]
    by_slot: OneToMany[CallSite, SlotBinding]
    by_type: OneToMany[CallId, FunctionId]


@dataclass(kw_only=True)
class Analysis:
    is_terminal: OneToOne[FunctionId, bool]
    function_exits: OneToMany[FunctionId, StatementId]
    parameter_types: OneToOne[ParameterId, Type]
    argument_types: OneToMany[SlotBinding, Type]


@dataclass
class SemanticModel:
    resolver: Resolver
    analysis: Analysis


def build_semantic_model(graph: Graph) -> SemanticModel:
    by_name = resolve_by_name(
        graph.nodes.calls,
        graph.indices.functions_by_name,
    )

    by_arity = resolve_by_arity(
        by_name,
        graph.nodes.calls,
        graph.nodes.functions,
    )

    by_slot = resolve_by_slot(
        by_arity,
        graph.nodes.calls,
        graph.nodes.functions,
        graph.nodes.arguments,
        graph.nodes.parameters,
    )

    parameter_types = collect_parameter_types(graph.nodes.parameters)
    argument_types = collect_argument_types(
        graph.nodes.arguments,
        by_slot,
        parameter_types,
    )

    by_type = resolve_by_type(by_slot, argument_types)
    is_terminal = collect_is_terminal(graph.nodes.functions)
    function_exits = collect_function_exits(
        graph.nodes.functions, graph.nodes.statements
    )

    return SemanticModel(
        resolver=Resolver(
            by_name=by_name,
            by_arity=by_arity,
            by_slot=by_slot,
            by_type=by_type,
        ),
        analysis=Analysis(
            parameter_types=parameter_types,
            argument_types=argument_types,
            is_terminal=is_terminal,
            function_exits=function_exits,
        ),
    )


def resolve_by_name(
    calls: Bidirectional[ast.CallStatement, CallId],
    functions_by_name: OneToMany[bytes, FunctionId],
) -> OneToMany[CallId, FunctionId]:
    out: Dict[CallId, List[FunctionId]] = {}

    for cid, call in calls.items():
        if targets := functions_by_name.get(call.name):
            out[cid] = targets

    return OneToMany(map=out)


def resolve_by_arity(
    call_targets: OneToMany[CallId, FunctionId],
    calls: Bidirectional[ast.CallStatement, CallId],
    functions: Bidirectional[ast.Function, FunctionId],
) -> OneToMany[CallId, FunctionId]:

    out: Dict[CallId, List[FunctionId]] = {}

    for cid, fids in call_targets.items():
        keep: List[FunctionId] = []

        call = calls.get_by_id(cid)
        argc = len(call.arguments)

        for fid in fids:
            fn = functions.get_by_id(fid)
            if len(fn.parameters) == argc:
                keep.append(fid)

        if keep:
            out[cid] = keep

    return OneToMany(map=out)


def resolve_by_slot(
    call_targets: OneToMany[CallId, FunctionId],
    calls: Bidirectional[ast.CallStatement, CallId],
    functions: Bidirectional[ast.Function, FunctionId],
    arguments: Bidirectional[ast.Argument, ArgumentId],
    parameters: Bidirectional[ast.Parameter, ParameterId],
) -> OneToMany[CallSite, SlotBinding]:

    out: Dict[CallSite, List[SlotBinding]] = {}

    for cid, fids in call_targets.items():
        call = calls.get_by_id(cid)

        for fid in fids:
            pairs: List[SlotBinding] = []
            function = functions.get_by_id(fid)

            for argument, parameter in zip(call.arguments, function.parameters):
                # find IDs behind argument and parameter
                aid = arguments.get_by_node(argument)
                pid = parameters.get_by_node(parameter)

                # append them as a pair
                pairs.append(SlotBinding(argument=aid, parameter=pid))

            out[CallSite(call=cid, function=fid)] = pairs

    return OneToMany(map=out)


def resolve_by_type(
    bindings: OneToMany[CallSite, SlotBinding],
    types: OneToMany[SlotBinding, Type],
) -> OneToMany[CallId, FunctionId]:

    out: Dict[CallId, List[FunctionId]] = {}

    for call_site, slots in bindings.items():
        ok = True

        # if any pair is not resolved to a type, reject this function
        # we expect all binding slots to have a type assigned

        for slot in slots:
            if not types.get(slot):
                ok = False
                break

        if ok:
            out.setdefault(call_site.call, []).append(call_site.function)

    return OneToMany(map=out)


def collect_parameter_types(
    parameters: Bidirectional[ast.Parameter, ParameterId],
) -> OneToOne[ParameterId, Type]:
    out: Dict[ParameterId, Type] = {}

    for pid, parameter in parameters.items():
        out[pid] = Type(name=parameter.type.name)

    return OneToOne(map=out)


def collect_argument_types(
    arguments: Bidirectional[ast.Argument, ArgumentId],
    bindings: OneToMany[CallSite, SlotBinding],
    parameter_types: OneToOne[ParameterId, Type],
) -> OneToMany[SlotBinding, Type]:
    out: Dict[SlotBinding, List[Type]] = {}

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

    for slots in bindings.values():
        for slot in slots:
            if ptype := parameter_types.find_by_id(slot.parameter):
                if argument := arguments.find_by_id(slot.argument):
                    if fits(argument.value, ptype):
                        out.setdefault(slot, []).append(ptype)

    return OneToMany(map=out)


def collect_is_terminal(
    functions: Bidirectional[ast.Function, FunctionId],
) -> OneToOne[FunctionId, bool]:
    out: Dict[FunctionId, bool] = {}

    for fid, function in functions.items():
        out[fid] = function.terminal

    return OneToOne(map=out)


def collect_function_exits(
    functions: Bidirectional[ast.Function, FunctionId],
    statements: Bidirectional[ast.Statement, StatementId],
) -> OneToMany[FunctionId, StatementId]:
    out: Dict[FunctionId, List[StatementId]] = {}

    for fid, function in functions.items():
        if len(function.statements) > 0:
            out[fid] = [statements.get_by_node(function.statements[-1])]

    return OneToMany(map=out)
