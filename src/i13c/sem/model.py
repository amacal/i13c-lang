from typing import Callable, Dict, List, Union

from i13c import ast
from i13c.sem import ids, nodes
from i13c.sem.graph import Graph
from i13c.sem.types import Register, Type


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
                ref=node.ref,
                mnemonic=node.mnemonic.name,
                operands=operands,
            )

        clobbers = [nodes.Register(name=clobber.name) for clobber in snippet.clobbers]
        instructions = [into_instructions(instr) for instr in snippet.instructions]

        exit_point = nodes.ExitPoint(
            ref=instructions[-1].ref if snippet.instructions else snippet.ref,
            statement=instructions[-1] if snippet.instructions else None,
        )

        out[snid] = nodes.Function(
            id=nodes.FunctionId(id=next()),
            kind="snippet",
            ref=snippet.ref,
            name=snippet.name,
            noreturn=snippet.noreturn,
            parameters=parameters,
            clobbers=clobbers,
            body=list(instructions),
            exit_points=[exit_point],
        )

    return out


def build_functions(
    graph: Graph,
    next: Callable[[], int],
) -> Dict[ids.FunctionId, nodes.Function]:
    out: Dict[ids.FunctionId, nodes.Function] = {}
    types: Dict[ids.ParameterId, Type] = {}

    for pid, parameter in graph.nodes.parameters.items():
        types[pid] = Type(name=parameter.type.name)

    for fid, function in graph.nodes.functions.items():
        parameters: List[nodes.Parameter] = []

        for pid in graph.edges.function_parameters.get(fid):
            param = graph.nodes.parameters.get_by_id(pid)

            parameters.append(
                nodes.Parameter(
                    id=nodes.ParameterId(id=next()),
                    name=param.name,
                    type=types[pid],
                    bind=None,
                )
            )

        out[fid] = nodes.Function(
            id=nodes.FunctionId(id=next()),
            kind="function",
            ref=function.ref,
            name=function.name,
            noreturn=function.noreturn,
            parameters=parameters,
            clobbers=[],
            body=[],
            exit_points=[],
        )

    return out


def build_calls(
    graph: Graph,
    functions: Dict[ids.FunctionId, nodes.Function],
    snippets: Dict[ids.SnippetId, nodes.Function],
    next: Callable[[], int],
) -> Dict[ids.CallId, nodes.Call]:
    out: Dict[ids.CallId, nodes.Call] = {}
    by_name: Dict[ids.CallId, List[Union[ids.FunctionId, ids.SnippetId]]] = {}

    for cid, call in graph.nodes.calls.items():
        found: List[Union[ids.FunctionId, ids.SnippetId]] = []

        if targets := graph.indices.functions_by_name.get(call.name):
            found.extend(targets)

        if targets := graph.indices.snippets_by_name.get(call.name):
            found.extend(targets)

        by_name[cid] = found

    for cid, call in graph.nodes.calls.items():
        arguments: List[nodes.Argument] = []
        candidates: List[nodes.Function] = []

        for aid in graph.edges.call_arguments.get(cid):
            argument = graph.nodes.arguments.get_by_id(aid)
            value = nodes.Literal(value=argument.value)

            # append argument node
            arguments.append(
                nodes.Argument(
                    id=nodes.ArgumentId(id=next()),
                    ref=argument.ref,
                    value=value,
                )
            )

        for fid in by_name[cid]:
            if isinstance(fid, ids.SnippetId):
                candidates.append(snippets[fid])
            else:
                candidates.append(functions[fid])

        out[cid] = nodes.Call(
            id=nodes.CallId(id=next()),
            ref=call.ref,
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

        exit_point = nodes.ExitPoint(
            ref=body[-1].ref if body else function.ref,
            statement=body[-1] if body else None,
        )

        function.body = body
        function.exit_points = [exit_point]


def merge_functions(
    snippets: Dict[ids.SnippetId, nodes.Function],
    functions: Dict[ids.FunctionId, nodes.Function],
) -> List[nodes.Function]:
    out: List[nodes.Function] = []

    out.extend(snippets.values())
    out.extend(functions.values())

    return out


def build_model(graph: Graph) -> List[nodes.Function]:
    next_id = 0

    def next() -> int:
        nonlocal next_id
        nid = next_id
        next_id += 1
        return nid

    snippets = build_snippets(graph, next)
    functions = build_functions(graph, next)

    calls = build_calls(
        graph,
        functions,
        snippets,
        next,
    )

    attach_bodies(graph, functions, calls)
    return merge_functions(snippets, functions)
