from collections.abc import Iterable

from i13c.core.generator import Generator
from i13c.core.graph import GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.encoding import encode
from i13c.semantic.typing.analyses.blocklets import Blocklet, BlockletId
from i13c.semantic.typing.analyses.entrypoints import Entrypoint
from i13c.semantic.typing.analyses.sections import Section, SectiontId
from i13c.semantic.typing.entities.signatures import SignatureId


def configure_sections() -> GraphNode:
    return GraphNode(
        builder=build_sections,
        constraint=None,
        produces=("analyses/sections",),
        requires=frozenset(
            {
                ("generator", "core/generator"),
                ("blocklets", "analyses/blocklets"),
                ("entrypoints", "analyses/entrypoints"),
            }
        ),
        views=GraphViews(list=ListExtractor),
    )


def build_sections(
    generator: Generator,
    blocklets: OneToOne[BlockletId, Blocklet],
    entrypoints: OneToOne[SignatureId, Entrypoint],
) -> OneToOne[SectiontId, Section]:
    sections: dict[SectiontId, Section] = {}
    entries: list[Blocklet] = []

    for entrypoint in entrypoints.values():
        for blocklet in blocklets.values():
            if blocklet.target == entrypoint.target.id:
                entries.append(blocklet)

    for blocklet in blocklets.values():
        if entries and blocklet != entries[0]:
            entries.append(blocklet)

    sections[SectiontId(value=generator.next())] = Section(
        type="text",
        data=encode(entries),
    )

    return OneToOne[SectiontId, Section].instance(sections)


class ListExtractor:
    def __init__(self, data: OneToOne[SectiontId, Section]):
        self.data = data

    def extract(
        self,
    ) -> Iterable[tuple[SectiontId, Section]]:
        yield from self.data.items()

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "id": "ID",
            "type": "Type",
            "len": "Length",
        }

    @staticmethod
    def rows(key: SectiontId, entry: Section) -> dict[str, str]:
        return {
            "id": key.identify(1),
            "type": entry.type,
            "len": str(len(entry.data)),
        }
