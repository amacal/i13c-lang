
from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToMany, OneToOne
from i13c.semantic.typing.entities.signatures import SignatureId
from i13c.semantic.typing.resolutions.signatures import SignatureAcceptance


def configure_signatures_by_names() -> GraphNode:
    return GraphNode(
        builder=build_signatures_by_names,
        constraint=None,
        produces=("indices/signatures/names",),
        requires=frozenset(
            {
                ("signatures", "resolutions/signatures/accepted"),
            }
        ),
    )


def build_signatures_by_names(
    signatures: OneToOne[SignatureId, SignatureAcceptance],
) -> OneToMany[bytes, SignatureAcceptance]:
    index: dict[bytes, list[SignatureAcceptance]] = {}

    for entry in signatures.values():
        data = index.get(entry.name)

        if data is None:
            index[entry.name] = [entry]
        else:
            data.append(entry)

    return OneToMany[bytes, SignatureAcceptance].instance(index)
