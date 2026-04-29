from typing import Dict, List

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToMany, OneToOne
from i13c.semantic.typing.entities.asmlets import Asmlet, AsmletId
from i13c.semantic.typing.entities.signatures import SignatureId


def configure_asmlets_by_signatures() -> GraphNode:
    return GraphNode(
        builder=build_asmlets_by_signatures,
        constraint=None,
        produces=("indices/asmlets/signatures",),
        requires=frozenset(
            {
                ("asmlets", "entities/asmlets"),
            }
        ),
    )


def build_asmlets_by_signatures(
    asmlets: OneToOne[AsmletId, Asmlet],
) -> OneToMany[SignatureId, Asmlet]:
    index: Dict[SignatureId, List[Asmlet]] = {}

    for _, entry in asmlets.items():
        data = index.get(entry.signature)

        if data is None:
            index[entry.signature] = [entry]
        else:
            data.append(entry)

    return OneToMany[SignatureId, Asmlet].instance(index)
