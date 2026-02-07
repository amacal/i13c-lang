from typing import Dict

from i13c import ast
from i13c.core.mapping import OneToOne
from i13c.sem.infra import Configuration
from i13c.sem.syntax import SyntaxGraph
from i13c.sem.typing.entities.operands import Operand, OperandId


def configure_operands() -> Configuration:
    return Configuration(
        builder=build_operands,
        produces=("entities/operands",),
        requires=frozenset({("graph", "syntax/graph")}),
    )


def build_operands(
    graph: SyntaxGraph,
) -> OneToOne[OperandId, Operand]:
    operands: Dict[OperandId, Operand] = {}

    for nid, operand in graph.operands.items():
        match operand:
            case ast.Register() as reg:
                target = Operand.register(operand.ref, reg.name)
            case ast.Immediate() as imm:
                target = Operand.immediate(operand.ref, imm.value)
            case ast.Reference() as ref:
                target = Operand.reference(operand.ref, ref.name)

        # derive operand ID from globally unique node ID
        operand_id = OperandId(value=nid.value)

        # append to operands map
        operands[operand_id] = target

    return OneToOne[OperandId, Operand].instance(operands)
