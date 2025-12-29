from typing import List, Optional, Union

from i13c import diag, ir, res, src
from i13c.sem.asm import Immediate, Instruction, Register
from i13c.sem.callsite import CallSiteId
from i13c.sem.entrypoint import EntryPoint
from i13c.sem.flowgraphs import FlowEntry, FlowGraph
from i13c.sem.function import FunctionId
from i13c.sem.literal import Hex
from i13c.sem.model import SemanticGraph
from i13c.sem.snippet import Slot, Snippet, SnippetId

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
    assert len(graph.entrypoints) == 1
    entrypoint = graph.entrypoints[0]

    for snid, snippet in graph.snippets.items():
        if not match_entrypoint(entrypoint, snid):
            continue

        # snippet may be live only if called directly
        codeblocks.append(lower_snippet(graph, snippet))
        entry = len(codeblocks) - 1

    for fid in graph.functions.keys():
        if fid not in graph.callable_live:
            continue

        next = len(codeblocks)
        flowgraph = graph.function_flowgraphs_live[fid]
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
    callsite = graph.callsites[cid]
    resolution = graph.callsite_resolutions[cid]

    # we know there is exactly one accepted resolution
    assert len(resolution.accepted) == 1
    acceptance = resolution.accepted[0]

    # we know we supported only snippet callsites
    assert acceptance.callable.kind == b"snippet"
    assert isinstance(acceptance.callable.target, SnippetId)
    snippet = graph.snippets[acceptance.callable.target]

    for binding in acceptance.bindings:
        # because this is a snippet callsite
        assert isinstance(binding.target, Slot)

        # we know all slots are literals for now
        assert binding.argument.kind == b"literal"
        literal = graph.literals[binding.argument.target]

        # we know all literals are hex for now
        assert literal.kind == b"hex"
        assert isinstance(literal.target, Hex)

        # extract register and immediate
        bind: Register = binding.target.bind
        imm: int = literal.target.value

        # emit move instruction for binding
        out.append(ir.MovRegImm(dst=IR_REGISTER_MAP[bind.name], imm=imm))

    # finally, emit snippet instructions
    for iid in snippet.instructions:
        instruction = graph.instructions[iid]
        out.append(lower_instruction(instruction))

    return out


def lower_snippet(graph: SemanticGraph, snippet: Snippet) -> ir.CodeBlock:
    out: List[ir.Instruction] = []

    for iid in snippet.instructions:
        instruction = graph.instructions[iid]
        out.append(lower_instruction(instruction))

    return ir.CodeBlock(
        instructions=out,
        terminator=ir.Stop(),
    )


def lower_instruction(instruction: Instruction) -> ir.Instruction:
    if instruction.mnemonic.name == b"mov":
        return lower_instruction_mov(instruction)

    elif instruction.mnemonic.name == b"syscall":
        return lower_instruction_syscall()

    raise UnsupportedMnemonic(instruction.ref, instruction.mnemonic.name)


def lower_instruction_mov(instruction: Instruction) -> ir.Instruction:
    dst = instruction.operands[0]
    src = instruction.operands[1]

    assert isinstance(dst.target, Register)
    assert isinstance(src.target, Immediate)

    dst_reg = IR_REGISTER_MAP[dst.target.name]
    src_imm = src.target.value

    return ir.MovRegImm(dst=dst_reg, imm=src_imm)


def lower_instruction_syscall() -> ir.Instruction:
    return ir.SysCall()
