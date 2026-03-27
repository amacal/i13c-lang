from typing import Dict

from i13c.core.dag import GraphNode
from i13c.core.generator import Generator
from i13c.core.mapping import OneToOne
from i13c.llvm.typing.registers import VirtualRegister
from i13c.semantic.typing.indices.variables import Variable, VariableId


def configure_registers() -> GraphNode:
    return GraphNode(
        builder=build_registers,
        constraint=None,
        produces=("llvm/registers",),
        requires=frozenset(
            {
                ("generator", "core/generator"),
                ("variables", "entities/variables"),
            }
        ),
    )


def build_registers(
    generator: Generator,
    variables: OneToOne[VariableId, Variable],
) -> OneToOne[VariableId, VirtualRegister]:
    registers: Dict[VariableId, VirtualRegister] = {}

    for vid in variables.keys():
        registers[vid] = VirtualRegister(id=generator.next())

    return OneToOne[VariableId, VirtualRegister](data=registers)
