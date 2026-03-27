from typing import Dict, Iterable, Tuple

from i13c.graph.artifacts import GraphArtifacts
from i13c.llvm.typing.blocks import Block
from i13c.llvm.typing.flows import BlockId
from i13c.llvm.typing.instructions import Instruction


class InstructionsListExtractor:
    @staticmethod
    def extract(
        artifacts: GraphArtifacts,
    ) -> Iterable[Tuple[BlockId, Block, int, Instruction]]:
        if llvm := artifacts.llvm_graph():
            for bid, instructions in llvm.instructions.items():
                for idx, instr in enumerate(instructions):
                    yield (bid, llvm.nodes.get(bid), idx, instr)

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "bid": "Block ID",
            "origin": "Origin",
            "idx": "Index",
            "instruction": "Instruction",
        }

    @staticmethod
    def rows(entry: Tuple[BlockId, Block, int, Instruction]) -> Dict[str, str]:
        return {
            "bid": entry[0].identify(1),
            "origin": str(entry[1].origin.identify(1)),
            "idx": str(entry[2]),
            "instruction": entry[3].native(),
        }
