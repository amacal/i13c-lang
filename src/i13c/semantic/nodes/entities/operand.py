from typing import Dict

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.immediates import ImmediateId
from i13c.semantic.typing.entities.operand import Operand, OperandId
from i13c.semantic.typing.entities.references import ReferenceId
from i13c.semantic.typing.entities.registers import RegisterId


def configure_operand() -> GraphNode:
    return GraphNode(
        builder=build_operands,
        constraint=None,
        produces=("entities/operand",),
        requires=frozenset({("graph", "syntax/graph")}),
    )


def build_operands(
    graph: SyntaxGraph,
) -> OneToOne[OperandId, Operand]:
    operands: Dict[OperandId, Operand] = {}

    # try all immediates
    for nid, node in graph.immediates.items():
        # derive operand ID from globally unique node ID
        operand_id = OperandId(value=nid.value)
        immediate_id = ImmediateId(value=nid.value)

        # append to operands map
        operands[operand_id] = Operand(
            ref=node.ref,
            kind="immediate",
            target=immediate_id,
        )

    # try all registers
    for nid, node in graph.registers.items():
        # derive operand ID from globally unique node ID
        operand_id = OperandId(value=nid.value)
        register_id = RegisterId(value=nid.value)

        # append to operands map
        operands[operand_id] = Operand(
            ref=node.ref,
            kind="register",
            target=register_id,
        )

    # try all references
    for nid, node in graph.references.items():
        # derive operand ID from globally unique node ID
        operand_id = OperandId(value=nid.value)
        reference_id = ReferenceId(value=nid.value)

        # append to operands map
        operands[operand_id] = Operand(
            ref=node.ref,
            kind="reference",
            target=reference_id,
        )

    return OneToOne[OperandId, Operand].instance(operands)
