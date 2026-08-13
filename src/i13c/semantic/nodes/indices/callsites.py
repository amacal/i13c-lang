
from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToMany, OneToOne
from i13c.semantic.typing.entities.callsites import CallSiteId
from i13c.semantic.typing.entities.signatures import SignatureId
from i13c.semantic.typing.entities.statements import StatementId
from i13c.semantic.typing.resolutions.callsites import CallSiteAcceptance


def configure_callsites_by_signatures() -> GraphNode:
    return GraphNode(
        builder=build_callsites_by_signatures,
        constraint=None,
        produces=("indices/callsites/signatures",),
        requires=frozenset(
            {
                ("callsites", "resolutions/callsites/accepted"),
            }
        ),
    )


def build_callsites_by_signatures(
    callsites: OneToOne[CallSiteId, CallSiteAcceptance],
) -> OneToMany[SignatureId, CallSiteAcceptance]:
    index: dict[SignatureId, list[CallSiteAcceptance]] = {}

    for entry in callsites.values():
        data = index.get(entry.signature.id)

        if data is None:
            index[entry.signature.id] = [entry]
        else:
            data.append(entry)

    return OneToMany[SignatureId, CallSiteAcceptance].instance(index)


def configure_callsites_by_statements() -> GraphNode:
    return GraphNode(
        builder=build_callsites_by_statements,
        constraint=None,
        produces=("indices/callsites/statements",),
        requires=frozenset(
            {
                ("callsites", "resolutions/callsites/accepted"),
            }
        ),
    )


def build_callsites_by_statements(
    callsites: OneToOne[CallSiteId, CallSiteAcceptance],
) -> OneToMany[StatementId, CallSiteAcceptance]:
    index: dict[StatementId, list[CallSiteAcceptance]] = {}

    for entry in callsites.values():
        data = index.get(entry.stmt)

        if data is None:
            index[entry.stmt] = [entry]
        else:
            data.append(entry)

    return OneToMany[StatementId, CallSiteAcceptance].instance(index)
