from typing import List

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.core import Identifier
from i13c.semantic.typing.entities.callsites import CallSite, CallSiteId
from i13c.semantic.typing.resolutions.callsites import CallSiteResolution
from i13c.syntax.source import SpanLike


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
) -> List[Diagnostic]:
    diagnostics: List[Diagnostic] = []

    for cid, resolution in resolutions.items():
        if not resolution.accepted:

            # truly missing if there are no rejected resolutions either
            if not resolution.rejected:
                diagnostics.append(
                    report_e3008_called_symbol_missing(
                        callsites.get(cid).ref,
                        callsites.get(cid).callee,
                    )
                )

    return diagnostics


def report_e3008_called_symbol_missing(
    ref: SpanLike, symbol: Identifier
) -> Diagnostic:
    return Diagnostic(
        ref=ref,
        code="E3008",
        message=f"Called symbol does not exist: '{symbol}'",
    )
