from typing import Dict, Iterable

from i13c.diag import Diagnostic
from i13c.graph.artifacts import GraphArtifacts


class SemanticListExtractor:
    @staticmethod
    def extract(artifacts: GraphArtifacts) -> Iterable[Diagnostic]:
        def inner() -> Iterable[Diagnostic]:
            for diagnostics in artifacts.rules().data.values():
                for diagnostic in diagnostics:
                    yield diagnostic

        return sorted(
            inner(), key=lambda x: (x.code, x.ref.offset, x.ref.length, x.message)
        )

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Reference",
            "code": "Rule Code",
            "name": "Rule Message",
        }

    @staticmethod
    def rows(entry: Diagnostic) -> Dict[str, str]:
        return {
            "ref": str(entry.ref) if entry.ref.offset and entry.ref.length else "",
            "code": entry.code,
            "name": entry.message.splitlines()[0].strip(),
        }
