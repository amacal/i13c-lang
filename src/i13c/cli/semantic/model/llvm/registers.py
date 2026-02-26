from dataclasses import dataclass
from typing import Dict, Iterable, Optional, Tuple

from i13c.graph.artifacts import GraphArtifacts
from i13c.lowering.typing.blocks import Registers
from i13c.lowering.typing.flows import BlockId
from i13c.lowering.typing.registers import reg_to_name


@dataclass(kw_only=True)
class RegistersContext:
    generated: Optional[Registers]
    inputs: Optional[Registers]
    used: Optional[Registers]
    clobbers: Optional[Registers]
    outputs: Optional[Registers]


class InstructionRegistersListExtractor:
    @staticmethod
    def extract(
        artifacts: GraphArtifacts,
    ) -> Iterable[Tuple[BlockId, int, RegistersContext]]:
        llvm = artifacts.llvm_graph()

        for bid in llvm.nodes.keys():
            for idx, (iid, _) in enumerate(llvm.flows.get(bid)):
                yield (
                    bid,
                    idx,
                    RegistersContext(
                        generated=llvm.iregs.generated.find(iid),
                        inputs=llvm.iregs.inputs.find(iid),
                        used=llvm.iregs.used.find(iid),
                        clobbers=llvm.iregs.clobbers.find(iid),
                        outputs=llvm.iregs.outputs.find(iid),
                    ),
                )

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "bid": "Block ID",
            "idx": "Index",
            "generated": "Generated",
            "inputs": "Inputs",
            "used": "Used",
            "clobbers": "Clobbers",
            "outputs": "Outputs",
        }

    @staticmethod
    def rows(
        entry: Tuple[BlockId, int, RegistersContext],
    ) -> Dict[str, str]:
        def format(registers: Optional[Registers]) -> str:
            return (
                " ".join(reg_to_name(reg) for reg in registers.items)
                if registers
                else ""
            )

        return {
            "bid": entry[0].identify(1),
            "idx": str(entry[1]),
            "generated": format(entry[2].generated),
            "inputs": format(entry[2].inputs),
            "used": format(entry[2].used),
            "clobbers": format(entry[2].clobbers),
            "outputs": format(entry[2].outputs),
        }


class BlockRegistersListExtractor:
    @staticmethod
    def extract(
        artifacts: GraphArtifacts,
    ) -> Iterable[Tuple[BlockId, RegistersContext]]:
        llvm = artifacts.llvm_graph()

        for bid in llvm.nodes.keys():
            yield (
                bid,
                RegistersContext(
                    generated=llvm.bregs.generated.find(bid),
                    inputs=llvm.bregs.inputs.find(bid),
                    used=llvm.bregs.used.find(bid),
                    clobbers=llvm.bregs.clobbers.find(bid),
                    outputs=llvm.bregs.outputs.find(bid),
                ),
            )

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "bid": "Block ID",
            "generated": "Generated",
            "inputs": "Inputs",
            "used": "Used",
            "clobbers": "Clobbers",
            "outputs": "Outputs",
        }

    @staticmethod
    def rows(
        entry: Tuple[BlockId, RegistersContext],
    ) -> Dict[str, str]:
        def format(registers: Optional[Registers]) -> str:
            return (
                " ".join(reg_to_name(reg) for reg in registers.items)
                if registers
                else ""
            )

        return {
            "bid": entry[0].identify(1),
            "generated": format(entry[1].generated),
            "inputs": format(entry[1].inputs),
            "used": format(entry[1].used),
            "clobbers": format(entry[1].clobbers),
            "outputs": format(entry[1].outputs),
        }
