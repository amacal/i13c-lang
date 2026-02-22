from typing import List

from i13c import diag, err
from i13c.core.dag import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.callsites import CallSite, CallSiteId
from i13c.semantic.typing.resolutions.callsites import CallSiteResolution


def configure_e3008() -> GraphNode:
    return GraphNode(
        builder=validate_called_symbol_exists,
        constraint=None,
        produces=("rules/e3008",),
        requires=frozenset(
            {
                ("callsites", "entities/callsites"),
                ("resolutions", "resolutions/callsites"),
            }
        ),
    )


def validate_called_symbol_exists(
    callsites: OneToOne[CallSiteId, CallSite],
    resolutions: OneToOne[CallSiteId, CallSiteResolution],
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for cid, resolution in resolutions.items():
        if not resolution.accepted:

            # truly missing if there are no rejected resolutions either
            if not resolution.rejected:
                diagnostics.append(
                    err.report_e3008_called_symbol_missing(
                        callsites.get(cid).ref,
                        callsites.get(cid).callee.name,
                    )
                )

    return diagnostics
