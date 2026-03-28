from typing import List, Optional, Union

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.callsites import CallSite, CallSiteId
from i13c.semantic.typing.entities.functions import Function, FunctionId
from i13c.semantic.typing.entities.snippets import Snippet, SnippetId
from i13c.semantic.typing.resolutions.callsites import CallSiteResolution
from i13c.syntax.source import SpanLike


def configure_e3007() -> GraphNode:
    return GraphNode(
        builder=validate_called_symbol_resolved,
        produces=("rules/e3007",),
        constraint=None,
        requires=frozenset(
            {
                ("functions", "entities/functions"),
                ("snippets", "entities/snippets"),
                ("callsites", "entities/callsites"),
                ("resolutions", "resolutions/callsites"),
            }
        ),
    )


def validate_called_symbol_resolved(
    functions: OneToOne[FunctionId, Function],
    snippets: OneToOne[SnippetId, Snippet],
    callsites: OneToOne[CallSiteId, CallSite],
    resolutions: OneToOne[CallSiteId, CallSiteResolution],
) -> List[Diagnostic]:
    diagnostics: List[Diagnostic] = []

    for cid, resolution in resolutions.items():
        if not resolution.accepted:

            # not resolved but some candidates were rejected
            if resolution.rejected:
                variants: List[str] = []

                for rejection in resolution.rejected:
                    reason = rejection.reason.decode()
                    callable = rejection.callable.target
                    target: Optional[Union[Function, Snippet]] = None

                    if rejection.callable.kind == b"function":
                        assert isinstance(callable, FunctionId)
                        target = functions.get(callable)

                    if rejection.callable.kind == b"snippet":
                        assert isinstance(callable, SnippetId)
                        target = snippets.get(callable)

                    assert target, "resolved callable must exist"
                    variants.append(f"{reason}: {target.signature()}")

                diagnostics.append(
                    report_e3007_no_matching_overload(
                        callsites.get(cid).ref,
                        callsites.get(cid).callee.name,
                        variants,
                    )
                )

    return diagnostics


def report_e3007_no_matching_overload(
    ref: SpanLike, name: bytes, candidates: List[str]
) -> Diagnostic:
    template = (
        "Called symbol '{name}' has no matching overload.\n"
        "Tried candidates:\n{candidates}"
    )

    args = dict(
        name=name.decode(),
        candidates="\n".join([f"  - {c}" for c in candidates]),
    )

    return Diagnostic(
        ref=ref,
        code="E3007",
        message=template.format(**args),
    )
