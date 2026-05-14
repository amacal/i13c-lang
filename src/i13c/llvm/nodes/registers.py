from typing import Dict

from i13c.core.generator import Generator
from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.llvm.typing.registers import VirtualRegister


def configure_registers() -> GraphNode:
    return GraphNode(
        builder=build_registers,
        constraint=None,
        produces=("llvm/registers",),
        requires=frozenset(
            {
                ("generator", "core/generator"),
            }
        ),
    )


def build_registers(
    generator: Generator,
) -> OneToOne[None, VirtualRegister]:
    registers: Dict[None, VirtualRegister] = {}

    return OneToOne[None, VirtualRegister](data=registers)
