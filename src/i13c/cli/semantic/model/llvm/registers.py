from typing import Dict, Iterable, Tuple

from i13c.graph.artifacts import GraphArtifacts
from i13c.lowering.typing.blocks import Registers
from i13c.lowering.typing.flows import BlockId
from i13c.lowering.typing.registers import reg_to_name


class RegistersListExtractor:
    @staticmethod
    def extract(
        artifacts: GraphArtifacts,
    ) -> Iterable[Tuple[BlockId, Registers, Registers, Registers]]:
        llvm = artifacts.llvm_graph()

        for bid in llvm.nodes.keys():
            yield (
                bid,
                llvm.registers.inputs.get(bid),
                llvm.registers.outputs.get(bid),
                llvm.registers.clobbers.get(bid),
            )

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "bid": "Block ID",
            "inputs": "Inputs",
            "outputs": "Outputs",
            "clobbers": "Clobbers",
        }

    @staticmethod
    def rows(entry: Tuple[BlockId, Registers, Registers, Registers]) -> Dict[str, str]:
        def format(registers: Registers) -> str:
            return ", ".join(reg_to_name(reg) for reg in registers.items)

        return {
            "bid": entry[0].identify(1),
            "inputs": format(entry[1]),
            "outputs": format(entry[2]),
            "clobbers": format(entry[3]),
        }
