from dataclasses import dataclass
from typing import Dict, Iterable, List, Set
from typing import Literal as Kind
from typing import Optional, Tuple, Union

from i13c import ast
from i13c.sem import ids, nodes
from i13c.sem.syntax import SyntaxGraph


@dataclass(kw_only=True)
class Identifier:
    name: bytes


@dataclass(kw_only=True, frozen=True)
class SnippetId:
    value: int


@dataclass(kw_only=True)
class Snippet:
    identifier: Identifier
    noreturn: bool
    slots: List[Slot]
    instructions: List[Instruction]


@dataclass(kw_only=True)
class Type:
    name: bytes


@dataclass(kw_only=True)
class Register:
    name: bytes


@dataclass(kw_only=True)
class Immediate:
    value: int


@dataclass(kw_only=True)
class Mnemonic:
    name: bytes


@dataclass(kw_only=True)
class Instruction:
    mnemonic: Mnemonic
    operands: List[Operand]


@dataclass(kw_only=True)
class Operand:
    kind: Kind[b"register", b"immediate"]
    target: Union[Register, Immediate]

    @staticmethod
    def register(name: bytes) -> "Operand":
        return Operand(kind=b"register", target=Register(name=name))

    @staticmethod
    def immediate(value: int) -> "Operand":
        return Operand(kind=b"immediate", target=Immediate(value=value))


@dataclass(kw_only=True)
class Slot:
    name: Identifier
    type: Type
    bind: Register


@dataclass(kw_only=True, frozen=True)
class FunctionId:
    value: int


Statement = Union["CallSiteId"]


@dataclass(kw_only=True)
class Function:
    identifier: Identifier
    noreturn: bool
    parameters: List[Parameter]
    statements: List[Statement]


@dataclass(kw_only=True)
class Parameter:
    name: Identifier
    type: Type


@dataclass(kw_only=True)
class Callable:
    kind: Kind[b"snippet", b"function"]
    target: Union[SnippetId, FunctionId]


@dataclass(kw_only=True, frozen=True)
class CallSiteId:
    value: int


@dataclass(kw_only=True)
class CallSite:
    callee: Identifier
    arguments: List[Argument]


@dataclass(kw_only=True)
class Argument:
    kind: Kind[b"literal"]
    target: LiteralId


@dataclass(kw_only=True, frozen=True)
class LiteralId:
    value: int


@dataclass(kw_only=True)
class Literal:
    kind: Kind[b"hex"]
    target: Hex


Width = Kind[8, 16, 32, 64]


@dataclass(kw_only=True)
class Hex:
    value: int
    width: Optional[Width]


RejectionReason = Kind[
    b"wrong-arity",
    b"type-mismatch",
]


@dataclass(kw_only=True)
class Rejection:
    callable: Callable
    reason: RejectionReason


@dataclass(kw_only=True)
class Acceptance:
    callable: Callable


@dataclass(kw_only=True)
class Resolution:
    accepted: List[Acceptance]
    rejected: List[Rejection]


@dataclass(kw_only=True)
class Terminality:
    noreturn: bool


@dataclass(kw_only=True, frozen=True)
class FlowEntry:
    pass


@dataclass(kw_only=True, frozen=True)
class FlowExit:
    pass


FlowNode = Union[FlowEntry, FlowExit, Statement]


@dataclass(kw_only=True)
class FlowGraph:
    entry: FlowEntry
    exit: FlowExit
    edges: Dict[FlowNode, List[FlowNode]]


@dataclass(kw_only=True)
class SemanticGraph:
    literals: Dict[LiteralId, Literal]
    snippets: Dict[SnippetId, Snippet]
    functions: Dict[FunctionId, Function]
    callsites: Dict[CallSiteId, CallSite]
    flowgraphs: Dict[FunctionId, FlowGraph]
    resolutions: Dict[CallSiteId, Resolution]
    terminalities: Dict[FunctionId, Terminality]


def build_semantic_graph(graph: SyntaxGraph) -> SemanticGraph:
    literals = build_semantic_graph_literals(graph)
    snippets = build_semantic_graph_snippets(graph)
    functions = build_semantic_graph_functions(graph)
    callsites = build_semantic_graph_callsites(graph)
    flowgraphs = build_semantic_graph_flowgraphs(functions)

    resolutions = build_semantic_graph_resolutions(
        functions,
        snippets,
        callsites,
        literals,
    )

    terminalities: Dict[FunctionId, Terminality] = {}

    return SemanticGraph(
        literals=literals,
        snippets=snippets,
        functions=functions,
        callsites=callsites,
        flowgraphs=flowgraphs,
        resolutions=resolutions,
        terminalities=terminalities,
    )


def build_semantic_graph_literals(
    graph: SyntaxGraph,
) -> Dict[LiteralId, Literal]:
    literals: Dict[LiteralId, Literal] = {}

    # integer out of range cannot be represented
    def derive_width(value: int) -> Optional[Width]:
        if value.bit_length() <= 8:
            return 8

        if value.bit_length() <= 16:
            return 16

        if value.bit_length() <= 32:
            return 32

        if value.bit_length() <= 64:
            return 64

        return None

    for nid, literal in graph.nodes.literals.items():
        assert isinstance(literal, ast.IntegerLiteral)

        # derive literal ID from globally unique node ID
        id = LiteralId(value=nid.value)

        literals[id] = Literal(
            kind=b"hex",
            target=Hex(
                value=literal.value,
                width=derive_width(literal.value),
            ),
        )

    return literals


def build_semantic_graph_snippets(graph: SyntaxGraph) -> Dict[SnippetId, Snippet]:
    snippets: Dict[SnippetId, Snippet] = {}

    for nid, snippet in graph.nodes.snippets.items():
        slots: List[Slot] = []
        instructions: List[Instruction] = []

        # derive snippet id from globally unique node id
        id = SnippetId(value=nid.value)

        for slot in snippet.slots:
            slots.append(
                Slot(
                    name=Identifier(name=slot.name),
                    type=Type(name=slot.type.name),
                    bind=Register(name=slot.bind.name),
                )
            )

        for instruction in snippet.instructions:
            operands: List[Operand] = []

            for operand in instruction.operands:
                match operand:
                    case ast.Register() as reg:
                        operands.append(Operand.register(name=reg.name))
                    case ast.Immediate() as imm:
                        operands.append(Operand.immediate(value=imm.value))

            instructions.append(
                Instruction(
                    mnemonic=Mnemonic(name=instruction.mnemonic.name),
                    operands=operands,
                )
            )

        snippets[id] = Snippet(
            identifier=Identifier(name=snippet.name),
            noreturn=snippet.noreturn,
            slots=slots,
            instructions=instructions,
        )

    return snippets


def build_semantic_graph_callsites(
    graph: SyntaxGraph,
) -> Dict[CallSiteId, CallSite]:
    callsites: Dict[CallSiteId, CallSite] = {}

    for nid, statement in graph.nodes.statements.items():
        arguments: List[Argument] = []

        # ignore non-call instructions
        # if not isinstance(statement, ast.CallStatement):
        #    continue

        # derive callsite id from globally unique node id
        id = CallSiteId(value=nid.value)

        for argument in statement.arguments:
            match argument:
                case ast.IntegerLiteral() as lit:
                    # find literal by AST node
                    lid = graph.nodes.literals.get_by_node(lit)

                    arguments.append(
                        Argument(
                            kind=b"literal",
                            target=LiteralId(value=lid.value),
                        )
                    )

        callsites[id] = CallSite(
            callee=Identifier(name=statement.name),
            arguments=arguments,
        )

    return callsites


def build_semantic_graph_functions(
    graph: SyntaxGraph,
) -> Dict[FunctionId, Function]:
    functions: Dict[FunctionId, Function] = {}

    for nid, function in graph.nodes.functions.items():
        parameters: List[Parameter] = []
        statements: List[Statement] = []

        # derive function id from globally unique node id
        id = FunctionId(value=nid.value)

        for parameter in function.parameters:
            parameters.append(
                Parameter(
                    name=Identifier(name=parameter.name),
                    type=Type(name=parameter.type.name),
                )
            )

        for statement in function.statements:
            sid = graph.nodes.statements.get_by_node(statement)
            statements.append(CallSiteId(value=sid.value))

        functions[id] = Function(
            identifier=Identifier(name=function.name),
            noreturn=function.noreturn,
            parameters=parameters,
            statements=statements,
        )

    return functions


def build_semantic_graph_flowgraphs(
    functions: Dict[FunctionId, Function],
) -> Dict[FunctionId, FlowGraph]:

    flowgraphs: Dict[FunctionId, FlowGraph] = {}

    for fid, function in functions.items():
        entry, exit = FlowEntry(), FlowExit()
        edges: Dict[FlowNode, List[FlowNode]] = {}

        if not function.statements:
            edges[entry] = [exit]

        else:

            stmts = function.statements
            edges[entry] = [stmts[0]]

            for predecessor, successor in zip(stmts, stmts[1:]):
                edges.setdefault(predecessor, []).append(successor)

            edges[stmts[-1]] = [exit]

        flowgraphs[fid] = FlowGraph(
            entry=entry,
            exit=exit,
            edges=edges,
        )

    return flowgraphs


def build_semantic_graph_resolutions(
    functions: Dict[FunctionId, Function],
    snippets: Dict[SnippetId, Snippet],
    callsites: Dict[CallSiteId, CallSite],
    literals: Dict[LiteralId, Literal],
) -> Dict[CallSiteId, Resolution]:
    resolutions: Dict[CallSiteId, Resolution] = {}

    def match_literal(literal: Literal, type: Type) -> bool:
        match (type.name, literal.kind):
            case (b"u8", b"hex"):
                assert isinstance(literal.target, Hex)
                return literal.target.width is not None and literal.target.width <= 8

            case (b"u16", b"hex"):
                assert isinstance(literal.target, Hex)
                return literal.target.width is not None and literal.target.width <= 16

            case (b"u32", b"hex"):
                assert isinstance(literal.target, Hex)
                return literal.target.width is not None and literal.target.width <= 32

            case (b"u64", b"hex"):
                assert isinstance(literal.target, Hex)
                return literal.target.width is not None and literal.target.width <= 64

            case _:
                return False

    def match_bindings(
        bindings: Iterable[Tuple[Argument, Type]],
    ) -> Optional[RejectionReason]:
        for argument, parameter in bindings:
            match argument:
                case Argument(kind=b"literal", target=lit):
                    assert isinstance(lit, LiteralId)
                    if not match_literal(literals[lit], type=parameter):
                        return b"type-mismatch"
                case _:
                    return b"type-mismatch"

        return None

    def match_function(
        callsite: CallSite, function: Function
    ) -> Optional[RejectionReason]:
        if len(function.parameters) != len(callsite.arguments):
            return b"wrong-arity"

        return match_bindings(
            zip(
                callsite.arguments,
                [parameter.type for parameter in function.parameters],
            )
        )

    def match_snippet(
        callsite: CallSite, snippet: Snippet
    ) -> Optional[RejectionReason]:
        if len(snippet.slots) != len(callsite.arguments):
            return b"wrong-arity"

        return match_bindings(
            zip(callsite.arguments, [slot.type for slot in snippet.slots])
        )

    def match_callable(
        callsite: CallSite, callable: Callable
    ) -> Optional[RejectionReason]:
        match callable:
            case Callable(kind=b"function", target=target):
                assert isinstance(target, FunctionId)
                return match_function(callsite, functions[target])
            case Callable(kind=b"snippet", target=target):
                assert isinstance(target, SnippetId)
                return match_snippet(callsite, snippets[target])
            case _:
                return None

    for cid, callsite in callsites.items():
        candidates: List[Callable] = []

        for fid, function in functions.items():
            if function.identifier == callsite.callee:
                candidates.append(
                    Callable(
                        kind=b"function",
                        target=fid,
                    )
                )

        for snid, snippet in snippets.items():
            if snippet.identifier == callsite.callee:
                candidates.append(
                    Callable(
                        kind=b"snippet",
                        target=snid,
                    )
                )

        reasoned: List[Tuple[Callable, Optional[RejectionReason]]] = [
            (candidate, match_callable(callsites[cid], candidate))
            for candidate in candidates
        ]

        resolutions[cid] = Resolution(
            accepted=[
                Acceptance(callable=candidate)
                for candidate, reason in reasoned
                if reason is None
            ],
            rejected=[
                Rejection(callable=candidate, reason=reason)
                for candidate, reason in reasoned
                if reason is not None
            ],
        )

    return resolutions


def build_semantic_graph_terminalities(
    snippets: Dict[SnippetId, Snippet],
    functions: Dict[FunctionId, Function],
    flowgraphs: Dict[FunctionId, FlowGraph],
    resolutions: Dict[CallSiteId, Resolution],
) -> Dict[FunctionId, Terminality]:

    def is_callable_terminal(callable: Callable) -> bool:
        match callable:
            case Callable(kind=b"snippet", target=target):
                assert isinstance(target, SnippetId)
                return snippets[target].noreturn

            case Callable(kind=b"function", target=target):
                assert isinstance(target, FunctionId)
                return terminalities[target].noreturn
            case _:
                return False

    def is_callsite_terminal(cid: CallSiteId) -> bool:
        resolution = resolutions[cid]

        if not resolution.accepted:
            return False

        for accepted in resolution.accepted:
            if not is_callable_terminal(accepted.callable):
                return False

        return True

    def has_path_to_exit(flowgraph: FlowGraph) -> bool:
        visited: Set[FlowNode] = set()
        stack: List[FlowNode] = [flowgraph.entry]

        while stack:
            node = stack.pop()

            if node in visited:
                continue

            visited.add(node)

            if node == flowgraph.exit:
                return True

            # if callsite is terminal, ignore its successors
            if isinstance(node, CallSiteId):
                if is_callsite_terminal(node):
                    continue

            # pick up successors
            for successor in flowgraph.edges.get(node, []):
                stack.append(successor)

        return False

    terminalities: Dict[FunctionId, Terminality] = {}

    for fid in functions.keys():
        terminalities[fid] = Terminality(noreturn=False)

    changed = True
    while changed:
        changed = False

        for fid in functions.keys():
            if terminalities[fid].noreturn:
                continue

            if not has_path_to_exit(flowgraphs[fid]):
                terminalities[fid] = Terminality(noreturn=True)
                changed = True

    return terminalities


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
