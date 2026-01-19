from typing import List

from i13c.lowering.graph import LowLevelContext
from i13c.lowering.nodes.registers import IR_REGISTER_MAP
from i13c.lowering.typing.instructions import Instruction, MovRegImm
from i13c.sem.typing.entities.literals import Hex, LiteralId
from i13c.sem.typing.entities.snippets import Slot
from i13c.sem.typing.resolutions.callsites import CallSiteBinding


def lower_callsite_bindings(
    ctx: LowLevelContext, bindings: List[CallSiteBinding]
) -> List[Instruction]:
    out: List[Instruction] = []

    for binding in bindings:
        # because this is a snippet callsite
        assert isinstance(binding.target, Slot)

        # we know all slots are literals for now
        assert binding.argument.kind == b"literal"
        assert isinstance(binding.argument.target, LiteralId)

        literal = ctx.graph.basic.literals.get(binding.argument.target)

        # we know all literals are hex for now
        assert literal.kind == b"hex"
        assert isinstance(literal.target, Hex)

        # extract slot binding
        bind = binding.target.bind
        imm: int = literal.target.value

        # emit move instruction for binding
        out.append(MovRegImm(dst=IR_REGISTER_MAP[bind.name], imm=imm))

    return out
