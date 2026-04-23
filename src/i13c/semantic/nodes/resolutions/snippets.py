from typing import Any, Dict, List

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.flags import FlagsId
from i13c.semantic.typing.entities.instructions import InstructionId
from i13c.semantic.typing.entities.signatures import SignatureId
from i13c.semantic.typing.entities.snippets import Snippet, SnippetId
from i13c.semantic.typing.resolutions.bindings import BindingAcceptance
from i13c.semantic.typing.resolutions.flags import FlagsAcceptance
from i13c.semantic.typing.resolutions.instructions import InstructionAcceptance
from i13c.semantic.typing.resolutions.signatures import SignatureAcceptance
from i13c.semantic.typing.resolutions.snippets import (
    SnippetAcceptance,
    SnippetRejection,
    SnippetResolution,
)


def configure_snippet_resolution() -> GraphGroup:
    resolve = GraphNode(
        builder=build_snippet_resolution,
        constraint=None,
        produces=("resolutions/snippets",),
        requires=frozenset(
            {
                ("snippets", "entities/snippets"),
                ("signatures", "resolutions/signatures/accepted"),
                ("instructions", "resolutions/instructions/accepted"),
                ("flags", "resolutions/flags/accepted"),
                ("bindings", "resolutions/bindings/accepted"),
            }
        ),
    )

    validate = GraphNode(
        builder=validate_snippet_resolution_e3015,
        constraint=None,
        produces=("rules/e3015",),
        requires=frozenset(
            {
                ("resolutions", "resolutions/snippets"),
            }
        ),
    )

    extract = GraphNode(
        builder=build_snippet_resolution_accepted,
        constraint=check_snippet_resolution_accepted,
        produces=("resolutions/snippets/accepted",),
        requires=frozenset(
            {
                ("rule_e3015", "rules/e3015"),
                ("resolutions", "resolutions/snippets"),
            }
        ),
    )

    return GraphGroup(nodes=[resolve, validate, extract])


def build_snippet_resolution(
    snippets: OneToOne[SnippetId, Snippet],
    signatures: OneToOne[SignatureId, SignatureAcceptance],
    instructions: OneToOne[InstructionId, InstructionAcceptance],
    flags: OneToOne[FlagsId, FlagsAcceptance],
    bindings: OneToOne[SignatureId, BindingAcceptance],
) -> OneToOne[SnippetId, SnippetResolution]:
    resolutions: Dict[SnippetId, SnippetResolution] = {}

    for sid, entry in snippets.items():
        resolution = SnippetResolution(
            accepted=[],
            rejected=[],
        )

        signature = signatures.get(entry.signature)
        binding = bindings.get(entry.signature)

        if entry.flags is not None:
            found_flags = flags.get(entry.flags)
        else:
            found_flags = None

        if len(resolution.rejected) == 0:
            resolution.accepted.append(
                SnippetAcceptance(
                    ref=entry.ref,
                    id=sid,
                    binding=binding,
                    flags=found_flags,
                    signature=signature,
                    instructions=[instructions.get(id) for id in entry.instructions],
                )
            )

        resolutions[sid] = resolution

    return OneToOne[SnippetId, SnippetResolution].instance(resolutions)


def check_snippet_resolution_accepted(
    rule_e3015: List[Diagnostic],
    **kwargs: Dict[str, Any],
) -> bool:
    return len(rule_e3015) == 0


def build_snippet_resolution_accepted(
    resolutions: OneToOne[SnippetId, SnippetResolution],
    **kwargs: Dict[str, Any],
) -> OneToOne[SnippetId, SnippetAcceptance]:
    accepted: Dict[SnippetId, SnippetAcceptance] = {}

    for id, resolution in resolutions.items():
        accepted[id] = resolution.accepted[0]

    return OneToOne[SnippetId, SnippetAcceptance].instance(accepted)


def validate_snippet_resolution_e3015(
    resolutions: OneToOne[SnippetId, SnippetResolution],
) -> List[Diagnostic]:
    diagnostics: List[Diagnostic] = []

    for id, resolution in resolutions.items():
        if len(resolution.accepted) != 1:
            for rejection in resolution.rejected:
                diagnostics.append(
                    report_snippet_resolution_e3015(rejection)
                )

    return diagnostics


def report_snippet_resolution_e3015(
    rejection: SnippetRejection,
) -> Diagnostic:
    return Diagnostic(
        ref=rejection.ref,
        code="E3015",
        message=f"Unresolved snippet {rejection.id}, reason: {rejection.reason}.",
    )
