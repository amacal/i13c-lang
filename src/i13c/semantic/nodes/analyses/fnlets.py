from collections.abc import Iterable

from i13c.core.graph import GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.analyses.cflows import FlowNode
from i13c.semantic.typing.analyses.dflows import DataFlows
from i13c.semantic.typing.analyses.fnlets import Fnlet, FnletBlock, FnletInstruction
from i13c.semantic.typing.analyses.llvm import EPILOG, PROLOG, Register
from i13c.semantic.typing.analyses.statements import StatementLlvm
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.entities.signatures import SignatureId
from i13c.semantic.typing.entities.statements import StatementId
from i13c.semantic.typing.resolutions.bindings import BindingAcceptance
from i13c.semantic.typing.resolutions.cflows import ControlFlowAcceptance
from i13c.semantic.typing.resolutions.functions import FunctionAcceptance
from i13c.syntax.source import Span


def configure_fnlets() -> GraphNode:
    return GraphNode(
        builder=build_fnlets,
        constraint=None,
        produces=("analyses/fnlets",),
        requires=frozenset(
            {
                ("cflows", "resolutions/cflows/accepted"),
                ("dflows", "analyses/dflows"),
                ("bindings", "resolutions/bindings/accepted"),
                ("statements", "analyses/statements"),
                ("functions", "resolutions/functions/accepted"),
            }
        ),
        views=GraphViews(list=ListExtractor),
    )


def build_fnlets(
    cflows: OneToOne[FunctionId, ControlFlowAcceptance],
    dflows: OneToOne[FunctionId, DataFlows],
    functions: OneToOne[FunctionId, FunctionAcceptance],
    statements: OneToOne[StatementId, StatementLlvm],
    bindings: OneToOne[SignatureId, BindingAcceptance],
) -> OneToOne[FunctionId, Fnlet]:
    fnlets: dict[FunctionId, Fnlet] = {}

    for fid, cflow in cflows.items():
        instructions: dict[int, list[FnletInstruction]] = {}
        cflow, dflow = cflows.get(fid), dflows.get(fid)

        emit_prolog(instructions, bindings, cflow, dflow)
        emit_body(instructions, statements, cflow)
        emit_epilog(instructions, cflow)

        blocks = [
            FnletBlock(instructions=instrs)
            for _, instrs in sorted(instructions.items())
        ]

        fnlets[fid] = Fnlet(
            ref=cflow.ref,
            target=fid,
            signature=functions.get(fid).signature,
            blocks=blocks,
        )

    return OneToOne[FunctionId, Fnlet].instance(fnlets)


def emit_prolog(
    instructions: dict[int, list[FnletInstruction]],
    bindings: OneToOne[SignatureId, BindingAcceptance],
    cflow: ControlFlowAcceptance,
    dflow: DataFlows,
):
    binding = bindings.get(cflow.signature)
    environment = cflow.environments[cflow.entry]

    binds = {
        dflow.vregs[dflow.values.index(environment[entry.src])]: Register(
            name=entry.dst
        )
        for entry in binding.mapping
    }

    instructions[0] = [
        PROLOG(
            operands=(),
            binds=binds,
            preserves=[
                Register(name=reg)
                for reg in (b"rbx", b"rbp", b"r12", b"r13", b"r14", b"r15")
            ],
        )
    ]


def emit_body(
    instructions: dict[int, list[FnletInstruction]],
    statements: OneToOne[StatementId, StatementLlvm],
    cflow: ControlFlowAcceptance,
):
    worklist: list[int] = [cflow.source.entry]

    while worklist:
        idx = worklist.pop()
        node = cflow.source.nodes[idx]

        # schedule direct successors
        worklist.extend(cflow.source.forward.get(idx, []))

        if not isinstance(node, FlowNode):
            continue

        # copy already emitted instructions
        entry = statements.get(node.target)
        segment = cflow.segments[idx] + 1

        if segment not in instructions:
            instructions[segment] = []

        instructions[segment].extend(entry.instructions)


def emit_epilog(
    instructions: dict[int, list[FnletInstruction]],
    cflow: ControlFlowAcceptance,
):
    segment = len(cflow.segments)

    if segment not in instructions:
        instructions[segment] = []

    instructions[segment].append(
        EPILOG(
            operands=(),
            preserves=[
                Register(name=reg)
                for reg in (b"rbx", b"rbp", b"r12", b"r13", b"r14", b"r15")
            ],
        )
    )


class ListExtractor:
    def __init__(self, data: OneToOne[FunctionId, Fnlet]):
        self.data = data

    def extract(
        self,
    ) -> Iterable[tuple[tuple[FunctionId, Span], tuple[int, FnletBlock]]]:
        for fid, fnlet in self.data.items():
            for idx, block in enumerate(fnlet.blocks):
                yield (fid, fnlet.ref), (idx, block)

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "function": "Function",
            "idx": "Index",
            "instrs": "Instructions",
        }

    @staticmethod
    def rows(
        key: tuple[FunctionId, Span], entry: tuple[int, FnletBlock]
    ) -> dict[str, str]:
        return {
            "ref": str(key[1]),
            "function": key[0].identify(1),
            "idx": str(entry[0]),
            "instrs": str(len(entry[1].instructions)),
        }
