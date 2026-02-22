from typing import Dict, Iterable, Tuple

from i13c.graph.artifacts import GraphArtifacts
from i13c.lowering.typing.blocks import Block
from i13c.lowering.typing.flows import BlockId
from i13c.semantic.typing.entities.functions import Function, FunctionId


class EntriesListExtractor:
    @staticmethod
    def extract(
        artifacts: GraphArtifacts,
    ) -> Iterable[Tuple[FunctionId, Function, BlockId, Block]]:
        llvm = artifacts.llvm_graph()
        semantic = artifacts.semantic_graph()

        for fid, bid in llvm.functions.entries.items():
            yield (fid, semantic.basic.functions.get(fid), bid, llvm.nodes.get(bid))

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "fid": "Function ID",
            "name": "Function Name",
            "bid": "Block ID",
            "terminator": "Terminator",
        }

    @staticmethod
    def rows(entry: Tuple[FunctionId, Function, BlockId, Block]) -> Dict[str, str]:
        return {
            "fid": entry[0].identify(1),
            "name": str(entry[1].identifier),
            "bid": entry[2].identify(1),
            "terminator": str(entry[3].terminator),
        }


class ExitsListExtractor:
    @staticmethod
    def extract(
        artifacts: GraphArtifacts,
    ) -> Iterable[Tuple[FunctionId, Function, BlockId, Block]]:
        llvm = artifacts.llvm_graph()
        semantic = artifacts.semantic_graph()

        for fid, bid in llvm.functions.exits.items():
            yield (fid, semantic.basic.functions.get(fid), bid, llvm.nodes.get(bid))

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "fid": "Function ID",
            "name": "Function Name",
            "bid": "Block ID",
            "terminator": "Terminator",
        }

    @staticmethod
    def rows(entry: Tuple[FunctionId, Function, BlockId, Block]) -> Dict[str, str]:
        return {
            "fid": entry[0].identify(1),
            "name": str(entry[1].identifier),
            "bid": entry[2].identify(1),
            "terminator": str(entry[3].terminator),
        }
