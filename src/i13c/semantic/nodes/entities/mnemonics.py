from typing import Dict

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.mnemonics import Mnemonic, MnemonicId


def configure_mnemonics() -> GraphNode:
    return GraphNode(
        builder=build_mnemonics,
        constraint=None,
        produces=("entities/mnemonics",),
        requires=frozenset({("graph", "syntax/graph")}),
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
