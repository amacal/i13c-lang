from typing import Dict, Iterable, Tuple

from i13c.core.graph import GraphNode, GraphViews
from i13c.core.mapping import OneToMany, OneToOne
from i13c.semantic.typing.analyses.entrypoints import Entrypoint
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.entities.signatures import SignatureId
from i13c.semantic.typing.entities.snippets import SnippetId
from i13c.semantic.typing.entities.statements import StatementId
from i13c.semantic.typing.resolutions.functions import FunctionAcceptance
from i13c.semantic.typing.resolutions.snippets import SnippetAcceptance


def configure_entrypoints() -> GraphNode:
    return GraphNode(
        builder=build_entrypoints,
        constraint=None,
        produces=("analyses/entrypoints",),
        requires=frozenset(
            {
                ("snippets", "resolutions/snippets/accepted"),
                ("functions", "resolutions/functions/accepted"),
                ("cgraphs", "analyses/cgraphs"),
            }
        ),
        views=GraphViews(list=ListExtractor),
    )


def build_entrypoints(
    snippets: OneToOne[SnippetId, SnippetAcceptance],
    functions: OneToOne[FunctionId, FunctionAcceptance],
    cgraphs: OneToMany[SignatureId, StatementId],
) -> OneToOne[SignatureId, Entrypoint]:
    entrypoints: Dict[SignatureId, Entrypoint] = {}

    for entry in snippets.values():
        if entry.signature.name == b"main":
            if len(entry.signature.parameters) == 0:
                if entry.noreturn:
                    entrypoints[entry.signature.id] = Entrypoint(target=entry)

    for entry in functions.values():
        if entry.signature.name == b"main":
            if len(entry.signature.parameters) == 0:
                if entry.noreturn:
                    entrypoints[entry.signature.id] = Entrypoint(target=entry)

    return OneToOne[SignatureId, Entrypoint].instance(entrypoints)


class ListExtractor:
    def __init__(self, data: OneToOne[SignatureId, Entrypoint]):
        self.data = data

    def extract(self) -> Iterable[Tuple[SignatureId, Entrypoint]]:
        for key, entry in self.data.items():
            yield key, entry

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Ref",
            "id": "Id",
            "target": "Target",
            "name": "Name",
        }

    @staticmethod
    def rows(key: SignatureId, entry: Entrypoint) -> Dict[str, str]:
        return {
            "ref": str(entry.target.ref),
            "id": key.identify(1),
            "target": entry.target.id.identify(1),
            "name": entry.target.signature.name.decode(),
        }
