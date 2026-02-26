from typing import Dict, Iterable, Tuple

from i13c.graph.artifacts import GraphArtifacts
from i13c.lowering.typing.abstracts import AbstractId, Abstracts
from i13c.lowering.typing.blocks import BlockId
from i13c.lowering.typing.flows import Flow, FlowId
from i13c.lowering.typing.instructions import Instruction, InstructionId


class PatchesOfStackFramesListExtractor:
    @staticmethod
    def extract(
        artifacts: GraphArtifacts,
    ) -> Iterable[Tuple[BlockId, FlowId, Flow, AbstractId, Abstracts]]:
        if llvm := artifacts.llvm_graph():
            for bid, instructions in llvm.flows.items():
                for iid, src in instructions:
                    if isinstance(iid, FlowId) and isinstance(src, Flow):
                        if instruction := llvm.patches.stackframes.find(iid):
                            yield (bid, iid, src, instruction[0], instruction[1])

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "bid": "Block ID",
            "fid": "Flow ID",
            "flow": "Flow",
            "aid": "Abstract ID",
            "abstracts": "Abstracts",
        }

    @staticmethod
    def rows(
        entry: Tuple[BlockId, FlowId, Flow, AbstractId, Abstracts],
    ) -> Dict[str, str]:
        return {
            "bid": entry[0].identify(1),
            "fid": entry[1].identify(1),
            "flow": entry[2].native(),
            "aid": entry[3].identify(1),
            "abstracts": entry[4].native(),
        }


class PatchesOfBindingsListExtractor:
    @staticmethod
    def extract(
        artifacts: GraphArtifacts,
    ) -> Iterable[Tuple[BlockId, FlowId, Flow, InstructionId, Instruction]]:
        if llvm := artifacts.llvm_graph():
            for bid, instructions in llvm.flows.items():
                for iid, src in instructions:
                    if isinstance(iid, FlowId) and isinstance(src, Flow):
                        if instruction := llvm.patches.bindings.find(iid):
                            yield (bid, iid, src, instruction[0], instruction[1])

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "bid": "Block ID",
            "fid": "Flow ID",
            "flow": "Flow",
            "iid": "Instruction ID",
            "instr": "Instruction",
        }

    @staticmethod
    def rows(
        entry: Tuple[BlockId, FlowId, Flow, InstructionId, Instruction],
    ) -> Dict[str, str]:
        return {
            "bid": entry[0].identify(1),
            "fid": entry[1].identify(1),
            "flow": entry[2].native(),
            "iid": entry[3].identify(1),
            "instr": entry[4].native(),
        }


class PatchesOfCallsitesListExtractor:
    @staticmethod
    def extract(
        artifacts: GraphArtifacts,
    ) -> Iterable[Tuple[BlockId, FlowId, Flow, InstructionId, Instruction]]:
        if llvm := artifacts.llvm_graph():
            for bid, instructions in llvm.flows.items():
                for iid, src in instructions:
                    if isinstance(iid, FlowId) and isinstance(src, Flow):
                        if instruction := llvm.patches.callsites.find(iid):
                            yield (bid, iid, src, instruction[0], instruction[1])

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "bid": "Block ID",
            "fid": "Flow ID",
            "flow": "Flow",
            "iid": "Instruction ID",
            "instr": "Instruction",
        }

    @staticmethod
    def rows(
        entry: Tuple[BlockId, FlowId, Flow, InstructionId, Instruction],
    ) -> Dict[str, str]:
        return {
            "bid": entry[0].identify(1),
            "fid": entry[1].identify(1),
            "flow": entry[2].native(),
            "iid": entry[3].identify(1),
            "instr": entry[4].native(),
        }


class PatchesOfSnapshotsListExtractor:
    @staticmethod
    def extract(
        artifacts: GraphArtifacts,
    ) -> Iterable[Tuple[BlockId, FlowId, Flow, InstructionId, Instruction]]:
        if llvm := artifacts.llvm_graph():
            for bid, instructions in llvm.flows.items():
                for iid, src in instructions:
                    if isinstance(iid, FlowId) and isinstance(src, Flow):
                        if instruction := llvm.patches.snapshots.find(iid):
                            yield (bid, iid, src, instruction[0], instruction[1])

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "bid": "Block ID",
            "fid": "Flow ID",
            "flow": "Flow",
            "iid": "Instruction ID",
            "instr": "Instruction",
        }

    @staticmethod
    def rows(
        entry: Tuple[BlockId, FlowId, Flow, InstructionId, Instruction],
    ) -> Dict[str, str]:
        return {
            "bid": entry[0].identify(1),
            "fid": entry[1].identify(1),
            "flow": entry[2].native(),
            "iid": entry[3].identify(1),
            "instr": entry[4].native(),
        }


class PatchesOfClobbersListExtractor:
    @staticmethod
    def extract(
        artifacts: GraphArtifacts,
    ) -> Iterable[Tuple[BlockId, FlowId, Flow, InstructionId, Instruction]]:
        if llvm := artifacts.llvm_graph():
            for bid, instructions in llvm.flows.items():
                for iid, src in instructions:
                    if isinstance(iid, FlowId) and isinstance(src, Flow):
                        if instruction := llvm.patches.clobbers.find(iid):
                            yield (bid, iid, src, instruction[0], instruction[1])

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "bid": "Block ID",
            "fid": "Flow ID",
            "flow": "Flow",
            "iid": "Instruction ID",
            "instr": "Instruction",
        }

    @staticmethod
    def rows(
        entry: Tuple[BlockId, FlowId, Flow, InstructionId, Instruction],
    ) -> Dict[str, str]:
        return {
            "bid": entry[0].identify(1),
            "fid": entry[1].identify(1),
            "flow": entry[2].native(),
            "iid": entry[3].identify(1),
            "instr": entry[4].native(),
        }
