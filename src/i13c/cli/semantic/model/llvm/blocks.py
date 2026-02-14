from typing import Dict, Iterable, Tuple

from i13c.graph.artifacts import GraphArtifacts
from i13c.lowering.typing.abstracts import Abstracts
from i13c.lowering.typing.blocks import Block, BlockInstruction
from i13c.lowering.typing.flows import BlockId, Flow


class BlockListExtractor:
    @staticmethod
    def extract(artifacts: GraphArtifacts) -> Iterable[Tuple[BlockId, Block]]:
        if llvm := artifacts.llvm_graph():
            return llvm.nodes.items()
        else:
            return []

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "id": "Block ID",
            "origin": "Origin",
            "terminator": "Terminator",
            "instructions": "Instructions",
        }

    @staticmethod
    def rows(entry: Tuple[BlockId, Block]) -> Dict[str, str]:
        return {
            "id": entry[0].identify(1),
            "origin": str(entry[1].origin.identify(1)),
            "terminator": str(entry[1].terminator),
            "instructions": str(len(entry[1].instructions)),
        }


class BlockInstructionsListExtractor:
    @staticmethod
    def extract(
        artifacts: GraphArtifacts,
    ) -> Iterable[Tuple[BlockId, Block, int, BlockInstruction]]:
        if llvm := artifacts.llvm_graph():
            for bid, block in llvm.nodes.items():
                for idx, instr in enumerate(block.instructions):
                    yield (bid, block, idx, instr)

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "bid": "Block ID",
            "origin": "Origin",
            "idx": "Index",
            "kind": "Kind",
            "instruction": "Instruction",
        }

    @staticmethod
    def rows(entry: Tuple[BlockId, Block, int, BlockInstruction]) -> Dict[str, str]:
        def into_kind(target: BlockInstruction) -> str:
            if isinstance(target, Abstracts):
                return "abstract"
            elif isinstance(target, Flow):
                return "flow"
            else:
                return "instruction"

        return {
            "bid": entry[0].identify(1),
            "origin": str(entry[1].origin.identify(1)),
            "idx": str(entry[2]),
            "kind": into_kind(entry[3]),
            "instruction": str(entry[3]),
        }
