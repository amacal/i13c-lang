from typing import Dict, Iterable, Tuple

from i13c.core.graph import GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.mnemonics import Mnemonic, MnemonicId


def configure_mnemonics() -> GraphNode:
    return GraphNode(
        builder=build_mnemonics,
        constraint=None,
        produces=("entities/mnemonics",),
        requires=frozenset({("graph", "syntax/graph")}),
        views=GraphViews(list=ListExtractor),
    )


def build_mnemonics(
    graph: SyntaxGraph,
) -> OneToOne[MnemonicId, Mnemonic]:
    mnemonics: Dict[MnemonicId, Mnemonic] = {}

    for mid, node in graph.snippet.mnemonics.items():
        mnemonic_id = MnemonicId(value=mid.value)

        # append to mnemonics map
        mnemonics[mnemonic_id] = Mnemonic(
            ref=node.ref,
            name=node.name,
        )

    return OneToOne[MnemonicId, Mnemonic].instance(mnemonics)

class ListExtractor:
    def __init__(self, data: OneToOne[MnemonicId, Mnemonic]):
        self.data = data

    def extract(self) -> Iterable[Tuple[MnemonicId, Mnemonic]]:
        for key, entry in self.data.items():
            yield key, entry

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "name": "Name",
        }

    @staticmethod
    def rows(key: MnemonicId, entry: Mnemonic) -> Dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "name": entry.name.decode(),
        }
