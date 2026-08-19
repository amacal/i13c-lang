from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.callsites import CallSiteId
from i13c.semantic.typing.entities.functions import Function, FunctionId
from i13c.semantic.typing.entities.signatures import SignatureId
from i13c.semantic.typing.resolutions.callsites import CallSiteAcceptance


def configure_functions_by_signatures() -> GraphNode:
    return GraphNode(
        builder=build_functions_by_signatures,
        constraint=None,
        produces=("indices/functions/signatures",),
        requires=frozenset(
            {
                ("functions", "entities/functions"),
            }
        ),
    )


def configure_functions_by_callsites() -> GraphNode:
    return GraphNode(
        builder=build_functions_by_callsites,
        constraint=None,
        produces=("indices/functions/callsites",),
        requires=frozenset(
            {
                ("functions", "indices/functions/signatures"),
                ("callsites", "resolutions/callsites/accepted"),
            }
        ),
    )


def build_functions_by_signatures(
    functions: OneToOne[FunctionId, Function],
) -> OneToOne[SignatureId, Function]:
    index: dict[SignatureId, Function] = {}

    for entry in functions.values():
        index[entry.signature] = entry

    return OneToOne[SignatureId, Function].instance(index)


def build_functions_by_callsites(
    functions: OneToOne[SignatureId, Function],
    callsites: OneToOne[CallSiteId, CallSiteAcceptance],
) -> OneToOne[CallSiteId, Function]:
    index: dict[CallSiteId, Function] = {}

    for eid, entry in callsites.items():
        if fn := functions.find(entry.signature.id):
            index[eid] = fn

    return OneToOne[CallSiteId, Function].instance(index)
