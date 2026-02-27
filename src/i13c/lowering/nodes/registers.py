from typing import Dict

from i13c.core.dag import GraphNode
from i13c.core.generator import Generator
from i13c.core.mapping import OneToOne
from i13c.lowering.typing.registers import VirtualRegister
from i13c.semantic.typing.entities.functions import Function, FunctionId
from i13c.semantic.typing.entities.parameters import ParameterId
from i13c.semantic.typing.indices.variables import VariableId


def configure_registers() -> GraphNode:
    return GraphNode(
        builder=build_registers,
        constraint=None,
        produces=("llvm/registers",),
        requires=frozenset(
            {
                ("generator", "core/generator"),
                ("functions", "entities/functions"),
                ("variables_by_parameter", "indices/variables-by-parameter"),
            }
        ),
    )


def build_registers(
    generator: Generator,
    functions: OneToOne[FunctionId, Function],
    variables_by_parameter: OneToOne[ParameterId, VariableId],
) -> OneToOne[VariableId, VirtualRegister]:
    registers: Dict[VariableId, VirtualRegister] = {}

    # collect all variables from function parameters
    # and assign them a virtual register to be used later

    for _, function in functions.items():
        for pid in function.parameters:
            variable = variables_by_parameter.get(pid)
            registers[variable] = VirtualRegister(id=generator.next())

    return OneToOne[VariableId, VirtualRegister](data=registers)
