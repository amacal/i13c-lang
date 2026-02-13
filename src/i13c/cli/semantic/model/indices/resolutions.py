from typing import Dict, Iterable, Tuple

from i13c.graph.artifacts import GraphArtifacts
from i13c.semantic.typing.entities.callsites import CallSite, CallSiteId
from i13c.semantic.typing.entities.instructions import Instruction, InstructionId
from i13c.semantic.typing.resolutions.callsites import CallSiteResolution
from i13c.semantic.typing.resolutions.instructions import InstructionResolution


class InstructionResolutionListExtractor:
    @staticmethod
    def extract(
        artifacts: GraphArtifacts,
    ) -> Iterable[Tuple[InstructionId, Instruction, InstructionResolution]]:
        return (
            (iid, artifacts.semantic_graph().basic.instructions.get(iid), resolution)
            for iid, resolution in artifacts.semantic_graph().indices.resolution_by_instruction.items()
        )

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "id": "Instruction ID",
            "mnemonic": "Mnemonic",
            "operands": "Operands",
            "accepted": "Accepted",
            "rejected": "Rejected",
        }

    @staticmethod
    def rows(
        entry: Tuple[InstructionId, Instruction, InstructionResolution],
    ) -> Dict[str, str]:
        return {
            "ref": str(entry[1].ref),
            "id": entry[0].identify(1),
            "mnemonic": str(entry[1].mnemonic),
            "operands": str(len(entry[1].operands)),
            "accepted": str(len(entry[2].accepted)),
            "rejected": str(len(entry[2].rejected)),
        }


class CallSiteResolutionListExtractor:
    @staticmethod
    def extract(
        artifacts: GraphArtifacts,
    ) -> Iterable[Tuple[CallSiteId, CallSite, CallSiteResolution]]:
        return (
            (cid, artifacts.semantic_graph().basic.callsites.get(cid), resolution)
            for cid, resolution in artifacts.semantic_graph().indices.resolution_by_callsite.items()
        )

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "id": "CallSite ID",
            "name": "Callee Name",
            "args": "Arguments",
            "accepted": "Accepted",
            "rejected": "Rejected",
        }

    @staticmethod
    def rows(
        entry: Tuple[CallSiteId, CallSite, CallSiteResolution],
    ) -> Dict[str, str]:
        return {
            "ref": str(entry[1].ref),
            "id": entry[0].identify(1),
            "name": str(entry[1].callee),
            "args": str(len(entry[1].arguments)),
            "accepted": str(len(entry[2].accepted)),
            "rejected": str(len(entry[2].rejected)),
        }
