from typing import Dict, Iterable, Tuple

from i13c.graph.artifacts import GraphArtifacts
from i13c.semantic.typing.entities.callsites import CallSite, CallSiteId
from i13c.semantic.typing.resolutions.callsites import (
    CallSiteAcceptance,
    CallSiteBinding,
    CallSiteResolution,
)


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


class AcceptedCallSiteResolutionListExtractor:
    @staticmethod
    def extract(
        artifacts: GraphArtifacts,
    ) -> Iterable[Tuple[CallSiteId, CallSite, int, CallSiteAcceptance]]:
        graph = artifacts.semantic_graph()

        return (
            (cid, graph.basic.callsites.get(cid), idx, acceptance)
            for cid, resolution in graph.indices.resolution_by_callsite.items()
            for idx, acceptance in enumerate(resolution.accepted)
        )

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "id": "CallSite ID",
            "name": "Callee Name",
            "idx": "Accepted Index",
            "target": "Accepted Target",
            "bindings": "Accepted Bindings",
        }

    @staticmethod
    def rows(
        entry: Tuple[CallSiteId, CallSite, int, CallSiteAcceptance],
    ) -> Dict[str, str]:
        return {
            "ref": str(entry[1].ref),
            "id": entry[0].identify(1),
            "name": str(entry[1].callee),
            "idx": str(entry[2]),
            "target": entry[3].callable.target.identify(1),
            "bindings": str(len(entry[3].bindings)),
        }


class BindingsOfCallSiteResolutionListExtractor:
    @staticmethod
    def extract(
        artifacts: GraphArtifacts,
    ) -> Iterable[
        Tuple[CallSiteId, CallSite, CallSiteResolution, int, CallSiteBinding]
    ]:
        graph = artifacts.semantic_graph()

        return (
            (cid, graph.basic.callsites.get(cid), resolution, idx, binding)
            for cid, resolution in graph.indices.resolution_by_callsite.items()
            for acceptance in resolution.accepted
            for idx, binding in enumerate(acceptance.bindings)
        )

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "id": "CallSite ID",
            "name": "Callee Name",
            "idx": "Binding Index",
            "kind": "Binding Kind",
        }

    @staticmethod
    def rows(
        entry: Tuple[CallSiteId, CallSite, CallSiteResolution, int, CallSiteBinding],
    ) -> Dict[str, str]:
        return {
            "ref": str(entry[1].ref),
            "id": entry[0].identify(1),
            "name": str(entry[1].callee),
            "idx": str(entry[3]),
            "kind": entry[4].kind.decode(),
        }
