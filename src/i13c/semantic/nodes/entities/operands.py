from typing import Dict

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.operands import (
    Offset,
    Operand,
    OperandId,
    Register,
)
from i13c.syntax import tree


def configure_operands() -> GraphNode:
    return GraphNode(
        builder=build_operands,
        constraint=None,
        produces=("entities/operands",),
        requires=frozenset({("graph", "syntax/graph")}),
    )


def build_operands(
    graph: SyntaxGraph,
) -> OneToOne[OperandId, Operand]:
    operands: Dict[OperandId, Operand] = {}

    for nid, operand in graph.operands.items():
        match operand:
            case tree.Register() as reg:
                target = Operand.register(operand.ref, reg.name)
            case tree.Immediate() as imm:
                target = Operand.immediate(operand.ref, imm.data)
            case tree.Reference() as ref:
                target = Operand.reference(operand.ref, ref.name)
            case tree.Address() as addr:
                target = Operand.address(
                    operand.ref,
                    Register.from_name(addr.base.name),
                    Offset.optional(
                        (addr.offset.kind, addr.offset.value.data)
                        if addr.offset is not None
                        else None
                    ),
                )

        # derive operand ID from globally unique node ID
        operand_id = OperandId(value=nid.value)

        # append to operands map
        operands[operand_id] = target

    return OneToOne[OperandId, Operand].instance(operands)
