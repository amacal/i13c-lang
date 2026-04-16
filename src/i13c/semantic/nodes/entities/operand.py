from typing import Dict

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.addresses import AddressId
from i13c.semantic.typing.entities.immediates import ImmediateId
from i13c.semantic.typing.entities.operand import Operand, OperandId
from i13c.semantic.typing.entities.references import ReferenceId
from i13c.semantic.typing.entities.registers import RegisterId
from i13c.syntax import tree


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
    for _, node in graph.operands.items():
        if isinstance(node, tree.snippet.Immediate):
            nid = graph.immediates.get_by_node(node)

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
    for _, node in graph.operands.items():
        if isinstance(node, tree.snippet.Register):
            nid = graph.registers.get_by_node(node)

            operand_id = OperandId(value=nid.value)
            register_id = RegisterId(value=nid.value)

            # append to operands map
            operands[operand_id] = Operand(
                ref=node.ref,
                kind="register",
                target=register_id,
            )

    # try all references
    for _, node in graph.operands.items():
        if isinstance(node, tree.snippet.Reference):
            nid = graph.references.get_by_node(node)

            # derive operand ID from globally unique node ID
            operand_id = OperandId(value=nid.value)
            reference_id = ReferenceId(value=nid.value)

            # append to operands map
            operands[operand_id] = Operand(
                ref=node.ref,
                kind="reference",
                target=reference_id,
            )

    # try all addresses
    for _, node in graph.operands.items():
        if isinstance(node, tree.snippet.Address):
            nid = graph.addresses.get_by_node(node)

            # derive operand ID from globally unique node ID
            operand_id = OperandId(value=nid.value)
            address_id = AddressId(value=nid.value)

            # append to operands map
            operands[operand_id] = Operand(
                ref=node.ref,
                kind="address",
                target=address_id,
            )

    return OneToOne[OperandId, Operand].instance(operands)
