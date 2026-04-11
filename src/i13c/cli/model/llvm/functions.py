from typing import Dict, Iterable, List, Tuple

from i13c.graph.artifacts import GraphArtifacts
from i13c.llvm.typing.blocks import Block, InstructionPosition
from i13c.llvm.typing.flows import BlockId
from i13c.llvm.typing.intervals import IntervalPressure, RegisterInterval
from i13c.llvm.typing.registers import reg64_to_name
from i13c.llvm.typing.stacks import StackFrame
from i13c.semantic.typing.entities.functions import Function, FunctionId


class EntriesListExtractor:
    @staticmethod
    def extract(
        artifacts: GraphArtifacts,
    ) -> Iterable[Tuple[FunctionId, Function, BlockId, Block]]:
        llvm = artifacts.llvm_graph()
        semantic = artifacts.semantic_graph()

        for fid, bid in llvm.functions.entries.items():
            yield (fid, semantic.entities.functions.get(fid), bid, llvm.nodes.get(bid))

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
            yield (fid, semantic.entities.functions.get(fid), bid, llvm.nodes.get(bid))

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


class BlocksListExtractor:
    @staticmethod
    def extract(
        artifacts: GraphArtifacts,
    ) -> Iterable[Tuple[FunctionId, Function, List[BlockId]]]:
        llvm = artifacts.llvm_graph()
        graph = artifacts.semantic_graph()

        for fid, blocks in llvm.functions.blocks.items():
            yield (fid, graph.entities.functions.get(fid), blocks)

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "fid": "Function ID",
            "name": "Function Name",
            "bids": "Block IDs",
        }

    @staticmethod
    def rows(entry: Tuple[FunctionId, Function, List[BlockId]]) -> Dict[str, str]:
        return {
            "fid": entry[0].identify(1),
            "name": str(entry[1].identifier),
            "bids": " ".join(bid.identify(1) for bid in entry[2]),
        }


class InstructionsInFunctionsListExtractor:
    @staticmethod
    def extract(
        artifacts: GraphArtifacts,
    ) -> Iterable[Tuple[FunctionId, Function, InstructionPosition]]:
        llvm = artifacts.llvm_graph()

        for fid, instr in llvm.functions.instructions.items():
            for instr in instr:
                yield (fid, artifacts.semantic_graph().entities.functions.get(fid), instr)

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "fid": "Function ID",
            "name": "Function Name",
            "bid": "Block ID",
            "idx": "Instruction Index",
            "instr": "Instruction",
        }

    @staticmethod
    def rows(entry: Tuple[FunctionId, Function, InstructionPosition]) -> Dict[str, str]:
        return {
            "fid": entry[0].identify(1),
            "name": str(entry[1].identifier),
            "bid": entry[2].block.identify(1),
            "idx": str(entry[2].index),
            "instr": entry[2].target.identify(1),
        }


class IntervalsInFunctionsListExtractor:
    @staticmethod
    def extract(
        artifacts: GraphArtifacts,
    ) -> Iterable[Tuple[FunctionId, Function, RegisterInterval]]:
        llvm = artifacts.llvm_graph()

        for fid, intervals in llvm.functions.intervals.items():
            for interval in intervals:
                yield (
                    fid,
                    artifacts.semantic_graph().entities.functions.get(fid),
                    interval,
                )

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "fid": "Function ID",
            "name": "Function Name",
            "reg": "Virtual Register",
            "start": "Interval Start",
            "end": "Interval End",
            "graph": "Interval Graph",
        }

    @staticmethod
    def rows(entry: Tuple[FunctionId, Function, RegisterInterval]) -> Dict[str, str]:
        return {
            "fid": entry[0].identify(1),
            "name": str(entry[1].identifier),
            "reg": reg64_to_name(entry[2].vreg),
            "start": str(entry[2].start),
            "end": str(entry[2].end),
            "graph": " " * entry[2].start + "*" * (entry[2].end - entry[2].start + 1),
        }


class IntervalPressureInFunctionsListExtractor:
    @staticmethod
    def extract(
        artifacts: GraphArtifacts,
    ) -> Iterable[Tuple[FunctionId, Function, IntervalPressure]]:
        llvm = artifacts.llvm_graph()

        for fid, pressure in llvm.functions.pressures.items():
            for entry in pressure:
                yield (
                    fid,
                    artifacts.semantic_graph().entities.functions.get(fid),
                    entry,
                )

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "fid": "Function ID",
            "name": "Function Name",
            "idx": "Interval Index",
            "pressure": "Interval Pressure",
            "registers": "Interval Registers",
        }

    @staticmethod
    def rows(entry: Tuple[FunctionId, Function, IntervalPressure]) -> Dict[str, str]:
        return {
            "fid": entry[0].identify(1),
            "name": str(entry[1].identifier),
            "idx": str(entry[2].index),
            "pressure": str(entry[2].pressure),
            "registers": " ".join(
                reg64_to_name(reg) for reg in sorted(entry[2].registers, reverse=True)
            ),
        }


class StackFrameInFunctionsListExtractor:
    @staticmethod
    def extract(
        artifacts: GraphArtifacts,
    ) -> Iterable[Tuple[FunctionId, Function, int, StackFrame]]:
        llvm = artifacts.llvm_graph()

        for fid, stackframe in llvm.functions.stacks.items():
            for idx in range(int(stackframe.size / 8)):
                yield (
                    fid,
                    artifacts.semantic_graph().entities.functions.get(fid),
                    idx,
                    stackframe,
                )

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "fid": "Function ID",
            "name": "Function Name",
            "size": "Stack Frame Size",
            "idx": "Stack Frame Slot",
            "regs": "Registers",
        }

    @staticmethod
    def rows(entry: Tuple[FunctionId, Function, int, StackFrame]) -> Dict[str, str]:
        return {
            "fid": entry[0].identify(1),
            "name": str(entry[1].identifier),
            "size": str(entry[3].size),
            "idx": str(entry[2]),
            "regs": " ".join(
                reg64_to_name(reg)
                for reg in sorted(entry[3].registers_at_slot(entry[2]), reverse=True)
            ),
        }
