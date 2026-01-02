from typing import List, Optional, Union

from i13c import diag, ir, res, src
from i13c.sem.model import SemanticGraph
from i13c.sem.typing.entities.callsites import CallSiteId
from i13c.sem.typing.entities.functions import FunctionId
from i13c.sem.typing.entities.instructions import Instruction
from i13c.sem.typing.entities.literals import Hex
from i13c.sem.typing.entities.operands import Immediate, Register
from i13c.sem.typing.entities.snippets import Slot, Snippet, SnippetId
from i13c.sem.typing.indices.entrypoints import EntryPoint
from i13c.sem.typing.indices.flowgraphs import FlowEntry, FlowGraph

# fmt: off
IR_REGISTER_MAP = {
    b"rax": 0, b"rcx": 1, b"rdx": 2, b"rbx": 3, b"rsp": 4, b"rbp": 5, b"rsi": 6, b"rdi": 7,
    b"r8": 8, b"r9": 9, b"r10": 10, b"r11": 11, b"r12": 12, b"r13": 13, b"r14": 14, b"r15": 15,
}
# fmt: on


class UnsupportedMnemonic(Exception):
    def __init__(self, ref: src.Span, name: bytes) -> None:
        self.ref = ref
        self.name = name


def match_entrypoint(
    entrypoint: EntryPoint, target: Union[SnippetId, FunctionId]
) -> bool:
    if entrypoint.kind == b"function":
        return entrypoint.target == target

    if entrypoint.kind == b"snippet":
        return entrypoint.target == target

    return False


def lower(graph: SemanticGraph) -> res.Result[ir.Unit, List[diag.Diagnostic]]:
    codeblocks: List[ir.CodeBlock] = []
    diagnostics: List[diag.Diagnostic] = []
    entry: Optional[int] = None

    # entrypoint always exists here
    assert graph.live.entrypoints.size() == 1
    _, entrypoint = graph.live.entrypoints.pop()

    for snid, snippet in graph.basic.snippets.items():
        if not match_entrypoint(entrypoint, snid):
            continue

        # snippet may be live only if called directly
        codeblocks.append(lower_snippet(graph, snippet))
        entry = len(codeblocks) - 1

    for fid in graph.basic.functions.keys():
        if fid not in graph.callable_live:
            continue

        next = len(codeblocks)
        flowgraph = graph.live.flowgraph_by_function.get(fid)
        codeblocks.extend(lower_function(graph, flowgraph, next))

        if match_entrypoint(entrypoint, fid):
            entry = len(codeblocks) - 1

    # any diagnostic is an error
    if diagnostics:
        return res.Err(diagnostics)

    # entrypoint must be found
    assert entry is not None

    return res.Ok(ir.Unit(entry=entry, codeblocks=codeblocks))


def lower_function(
    graph: SemanticGraph,
    flow: FlowGraph,
    next: int,
) -> List[ir.CodeBlock]:
    out: List[ir.CodeBlock] = []

    # remove entry and exit from nodes
    nodes = [node for node in flow.edges.keys() if node not in (flow.entry, flow.exit)]

    # assign ids to nodes, entry/exit won't get ids
    ids = {node: next + idx for idx, node in enumerate(nodes)}

    for node, successors in flow.edges.items():
        instructions: List[ir.Instruction] = []
        terminator: ir.Terminator

        if isinstance(node, FlowEntry):
            continue

        # node is a callsite
        if isinstance(node, CallSiteId):
            instructions.extend(lower_callsite(graph, node))

        if not successors:
            terminator = ir.Stop()
        else:
            # we don't handle multiple successors
            assert len(successors) == 1
            terminator = ir.FallThrough(target=ids[successors[0]])

        out.append(
            ir.CodeBlock(
                instructions=instructions,
                terminator=terminator,
            )
        )

    return out


def lower_callsite(graph: SemanticGraph, cid: CallSiteId) -> List[ir.Instruction]:

    out: List[ir.Instruction] = []

    # find callsite and its resolution
    callsite = graph.basic.callsites.get(cid)
    resolution = graph.indices.resolution_by_callsite.get(cid)

    # we know there is exactly one accepted resolution
    assert len(resolution.accepted) == 1
    acceptance = resolution.accepted[0]

    # we know we supported only snippet callsites
    assert acceptance.callable.kind == b"snippet"
    assert isinstance(acceptance.callable.target, SnippetId)
    snippet = graph.basic.snippets.get(acceptance.callable.target)

    for binding in acceptance.bindings:
        # because this is a snippet callsite
        assert isinstance(binding.target, Slot)

        # we know all slots are literals for now
        assert binding.argument.kind == b"literal"
        literal = graph.basic.literals.get(binding.argument.target)

        # we know all literals are hex for now
        assert literal.kind == b"hex"
        assert isinstance(literal.target, Hex)

        # extract slot binding
        bind = binding.target.bind
        imm: int = literal.target.value

        # emit move instruction for binding
        if bind.kind == b"register":
            out.append(ir.MovRegImm(dst=IR_REGISTER_MAP[bind.name], imm=imm))

    # finally, emit snippet instructions
    for iid in snippet.instructions:
        instruction = graph.basic.instructions.get(iid)
        out.append(lower_instruction(graph, instruction))

    return out


def lower_snippet(graph: SemanticGraph, snippet: Snippet) -> ir.CodeBlock:
    out: List[ir.Instruction] = []

    for iid in snippet.instructions:
        instruction = graph.basic.instructions.get(iid)
        out.append(lower_instruction(graph, instruction))

    return ir.CodeBlock(
        instructions=out,
        terminator=ir.Stop(),
    )


def lower_instruction(graph: SemanticGraph, instruction: Instruction) -> ir.Instruction:
    if instruction.mnemonic.name == b"mov":
        return lower_instruction_mov(graph, instruction)

    elif instruction.mnemonic.name == b"shl":
        return lower_instruction_shl(graph, instruction)

    elif instruction.mnemonic.name == b"syscall":
        return lower_instruction_syscall()

    raise UnsupportedMnemonic(instruction.ref, instruction.mnemonic.name)


def lower_instruction_mov(
    graph: SemanticGraph, instruction: Instruction
) -> ir.Instruction:
    dst = graph.basic.operands.get(instruction.operands[0])
    src = graph.basic.operands.get(instruction.operands[1])

    assert isinstance(dst.target, Register)
    assert isinstance(src.target, Immediate)

    dst_reg = IR_REGISTER_MAP[dst.target.name]
    src_imm = src.target.value

    return ir.MovRegImm(dst=dst_reg, imm=src_imm)


def lower_instruction_shl(
    graph: SemanticGraph, instruction: Instruction
) -> ir.Instruction:

    dst_id = instruction.operands[0]
    src_id = instruction.operands[1]

    dst = graph.basic.operands.get(dst_id).target
    src = graph.basic.operands.get(src_id).target

    if resolution := graph.indices.resolution_by_operand.find(dst_id):
        dst = resolution.accepted[0].target

    if resolution := graph.indices.resolution_by_operand.find(src_id):
        src = resolution.accepted[0].target

    assert isinstance(dst, Register)
    assert isinstance(src, Immediate)

    dst_reg = IR_REGISTER_MAP[dst.name]
    src_imm = src.value

    return ir.ShlRegImm(dst=dst_reg, imm=src_imm)


def lower_instruction_syscall() -> ir.Instruction:
    return ir.SysCall()
