from dataclasses import dataclass
from typing import Callable, Dict, List, Union

from i13c import ast
from i13c.sem import ids, nodes
from i13c.sem.core import Bidirectional, OneToMany, OneToOne
from i13c.sem.graph import Graph
from i13c.sem.types import CallSite, Register, SlotBinding, Type


@dataclass
class Resolver:
    by_name: OneToMany[ids.CallId, Union[ids.FunctionId, ids.SnippetId]]
    by_arity: OneToMany[ids.CallId, ids.FunctionId]
    by_slot: OneToMany[CallSite, SlotBinding]
    by_type: OneToMany[ids.CallId, ids.FunctionId]


@dataclass(kw_only=True)
class Analysis:
    is_terminal: OneToOne[ids.FunctionId, bool]
    function_exits: OneToMany[ids.FunctionId, ids.StatementId]
    parameter_types: OneToOne[ids.ParameterId, Type]
    argument_types: OneToMany[SlotBinding, Type]


@dataclass
class SemanticModel:
    resolver: Resolver
    analysis: Analysis
    functions: List[nodes.Function]


def build_semantic_model(graph: Graph) -> SemanticModel:
    by_name = resolve_by_name(
        graph.nodes.calls,
        graph.indices.functions_by_name,
        graph.indices.snippets_by_name,
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
        functions=[],
    )


def build_snippets(
    graph: Graph,
    next: Callable[[], int],
) -> Dict[ids.SnippetId, nodes.Function]:
    out: Dict[ids.SnippetId, nodes.Function] = {}

    for snid, snippet in graph.nodes.snippets.items():
        parameters: List[nodes.Parameter] = []

        for sid in graph.edges.snippet_slots.get(snid):
            slot = graph.nodes.slots.get_by_id(sid)

            parameters.append(
                nodes.Parameter(
                    id=nodes.ParameterId(id=next()),
                    name=slot.name,
                    type=Type(name=slot.type.name),
                    bind=Register(name=slot.bind.name),
                )
            )

        def into_instructions(node: ast.Instruction) -> nodes.Instruction:
            operands: List[Union[nodes.Register, nodes.Immediate]] = []

            for operand in node.operands:
                match operand:
                    case ast.Register() as reg:
                        operands.append(nodes.Register(name=reg.name))
                    case ast.Immediate() as imm:
                        operands.append(nodes.Immediate(value=imm.value))

            return nodes.Instruction(
                id=nodes.InstructionId(id=next()),
                mnemonic=node.mnemonic.name,
                operands=operands,
            )

        clobbers = [nodes.Register(name=clobber.name) for clobber in snippet.clobbers]
        instructions = (into_instructions(instr) for instr in snippet.instructions)

        out[snid] = nodes.Function(
            id=nodes.FunctionId(id=next()),
            name=snippet.name,
            terminal=snippet.terminal,
            parameters=parameters,
            clobbers=clobbers,
            body=list(instructions),
        )

    return out


def build_functions(
    graph: Graph,
    analysis: Analysis,
    next: Callable[[], int],
) -> Dict[ids.FunctionId, nodes.Function]:
    out: Dict[ids.FunctionId, nodes.Function] = {}

    for fid, function in graph.nodes.functions.items():
        parameters: List[nodes.Parameter] = []

        for pid in graph.edges.function_parameters.get(fid):
            param = graph.nodes.parameters.get_by_id(pid)

            parameters.append(
                nodes.Parameter(
                    id=nodes.ParameterId(id=next()),
                    name=param.name,
                    type=analysis.parameter_types.get_by_id(pid),
                    bind=None,
                )
            )

        out[fid] = nodes.Function(
            id=nodes.FunctionId(id=next()),
            name=function.name,
            terminal=analysis.is_terminal.get_by_id(fid),
            parameters=parameters,
            clobbers=[],
            body=[],
        )

    return out


def build_calls(
    graph: Graph,
    resolver: Resolver,
    functions: Dict[ids.FunctionId, nodes.Function],
    snippets: Dict[ids.SnippetId, nodes.Function],
    next: Callable[[], int],
) -> Dict[ids.CallId, nodes.Call]:
    out: Dict[ids.CallId, nodes.Call] = {}

    for cid, call in graph.nodes.calls.items():
        arguments: List[nodes.Argument] = []
        candidates: List[nodes.Function] = []

        for aid in graph.edges.call_arguments.get(cid):
            argument = graph.nodes.arguments.get_by_id(aid)
            value = nodes.Literal(value=argument.value)

            # append argument node
            arguments.append(
                nodes.Argument(id=nodes.ArgumentId(id=next()), value=value)
            )

        for fid in resolver.by_name.get(cid):
            if isinstance(fid, ids.SnippetId):
                candidates.append(snippets[fid])
            else:
                candidates.append(functions[fid])

        out[cid] = nodes.Call(
            id=nodes.CallId(id=next()),
            name=call.name,
            arguments=arguments,
            candidates=candidates,
        )

    return out


def attach_bodies(
    graph: Graph,
    functions: Dict[ids.FunctionId, nodes.Function],
    calls: Dict[ids.CallId, nodes.Call],
) -> None:
    for fid, function in functions.items():
        body: List[Union[nodes.Instruction, nodes.Call]] = []

        for sid in graph.edges.function_statements.get(fid):
            call = graph.edges.statement_calls.find_by_id(sid)

            if call is not None:
                body.append(calls[call])

        function.body = body


def merge_functions(
    snippets: Dict[nodes.FunctionId, nodes.Function],
    functions: Dict[ids.FunctionId, nodes.Function],
) -> List[nodes.Function]:
    out: List[nodes.Function] = []

    out.extend(snippets.values())
    out.extend(functions.values())

    return out


def resolve_by_name(
    calls: Bidirectional[ast.CallStatement, ids.CallId],
    functions_by_name: OneToMany[bytes, ids.FunctionId],
    snippets_by_name: OneToMany[bytes, ids.SnippetId],
) -> OneToMany[ids.CallId, Union[ids.FunctionId, ids.SnippetId]]:
    out: Dict[ids.CallId, List[Union[ids.FunctionId, ids.SnippetId]]] = {}

    for cid, call in calls.items():
        candidates: List[Union[ids.FunctionId, ids.SnippetId]] = []

        if targets := functions_by_name.get(call.name):
            candidates.extend(targets)

        if targets := snippets_by_name.get(call.name):
            candidates.extend(targets)

        out[cid] = candidates

    return OneToMany(map=out)


def resolve_by_arity(
    call_targets: OneToMany[ids.CallId, Union[ids.FunctionId, ids.SnippetId]],
    calls: Bidirectional[ast.CallStatement, ids.CallId],
    functions: Bidirectional[ast.Function, ids.FunctionId],
) -> OneToMany[ids.CallId, ids.FunctionId]:

    out: Dict[ids.CallId, List[ids.FunctionId]] = {}

    for cid, fids in call_targets.items():
        keep: List[ids.FunctionId] = []

        call = calls.get_by_id(cid)
        argc = len(call.arguments)

        for fid in fids:
            if isinstance(fid, ids.FunctionId):
                fn = functions.get_by_id(fid)
                if len(fn.parameters) == argc:
                    keep.append(fid)

        if keep:
            out[cid] = keep

    return OneToMany(map=out)


def resolve_by_slot(
    call_targets: OneToMany[ids.CallId, ids.FunctionId],
    calls: Bidirectional[ast.CallStatement, ids.CallId],
    functions: Bidirectional[ast.Function, ids.FunctionId],
    arguments: Bidirectional[ast.Argument, ids.ArgumentId],
    parameters: Bidirectional[ast.Parameter, ids.ParameterId],
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
) -> OneToMany[ids.CallId, ids.FunctionId]:

    out: Dict[ids.CallId, List[ids.FunctionId]] = {}

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
    parameters: Bidirectional[ast.Parameter, ids.ParameterId],
) -> OneToOne[ids.ParameterId, Type]:
    out: Dict[ids.ParameterId, Type] = {}

    for pid, parameter in parameters.items():
        out[pid] = Type(name=parameter.type.name)

    return OneToOne(map=out)


def collect_argument_types(
    arguments: Bidirectional[ast.Argument, ids.ArgumentId],
    bindings: OneToMany[CallSite, SlotBinding],
    parameter_types: OneToOne[ids.ParameterId, Type],
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
    functions: Bidirectional[ast.Function, ids.FunctionId],
) -> OneToOne[ids.FunctionId, bool]:
    out: Dict[ids.FunctionId, bool] = {}

    for fid, function in functions.items():
        out[fid] = function.terminal

    return OneToOne(map=out)


def collect_function_exits(
    functions: Bidirectional[ast.Function, ids.FunctionId],
    statements: Bidirectional[ast.Statement, ids.StatementId],
) -> OneToMany[ids.FunctionId, ids.StatementId]:
    out: Dict[ids.FunctionId, List[ids.StatementId]] = {}

    for fid, function in functions.items():
        if len(function.statements) > 0:
            out[fid] = [statements.get_by_node(function.statements[-1])]

    return OneToMany(map=out)
