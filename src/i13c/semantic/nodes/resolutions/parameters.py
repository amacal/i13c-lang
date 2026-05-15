from typing import Any, Dict, List

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.parameters import Parameter, ParameterId
from i13c.semantic.typing.entities.types import TypeId
from i13c.semantic.typing.resolutions.binds import BindAcceptance
from i13c.semantic.typing.resolutions.parameters import (
    ParameterAcceptance,
    ParameterBind,
    ParameterResolution,
)
from i13c.semantic.typing.resolutions.types import TypeAcceptance


def configure_parameter_resolution() -> GraphGroup:
    resolve = GraphNode(
        builder=build_parameter_resolution,
        constraint=None,
        produces=("resolutions/parameters",),
        requires=frozenset(
            {
                ("parameters", "entities/parameters"),
                ("types", "resolutions/types/accepted"),
                ("binds", "indices/binds/parameters"),
            }
        ),
    )

    validate = GraphNode(
        builder=validate_parameter_resolution_e3014,
        constraint=None,
        produces=("rules/e3014",),
        requires=frozenset(
            {
                ("parameters", "entities/parameters"),
                ("resolutions", "resolutions/parameters"),
            }
        ),
    )

    extract = GraphNode(
        builder=build_parameter_resolution_accepted,
        constraint=check_parameter_resolution_accepted,
        produces=("resolutions/parameters/accepted",),
        requires=frozenset(
            {
                ("rule_e3014", "rules/e3014"),
                ("resolutions", "resolutions/parameters"),
            }
        ),
    )

    return GraphGroup(nodes=[resolve, validate, extract])


def build_parameter_resolution(
    parameters: OneToOne[ParameterId, Parameter],
    types: OneToOne[TypeId, TypeAcceptance],
    binds: OneToOne[ParameterId, BindAcceptance],
) -> OneToOne[ParameterId, ParameterResolution]:
    resolutions: Dict[ParameterId, ParameterResolution] = {}

    for pid, entry in parameters.items():
        resolution = ParameterResolution(
            accepted=[],
            rejected=[],
        )

        bind_type: ParameterBind = "value"

        if bind := binds.find(pid):
            bind_type = "literal" if bind.is_immediate() else "value"

        resolution.accepted.append(
            ParameterAcceptance(
                ref=entry.ref,
                id=pid,
                name=entry.name,
                type=types.get(entry.type),
                bind=bind_type,
            )
        )

        resolutions[pid] = resolution

    return OneToOne[ParameterId, ParameterResolution].instance(resolutions)


def check_parameter_resolution_accepted(
    rule_e3014: List[Diagnostic],
    **kwargs: Dict[str, Any],
) -> bool:
    return len(rule_e3014) == 0


def build_parameter_resolution_accepted(
    resolutions: OneToOne[ParameterId, ParameterResolution],
    **kwargs: Dict[str, Any],
) -> OneToOne[ParameterId, ParameterAcceptance]:
    accepted: Dict[ParameterId, ParameterAcceptance] = {}

    for id, resolution in resolutions.items():
        accepted[id] = resolution.accepted[0]

    return OneToOne[ParameterId, ParameterAcceptance].instance(accepted)


def validate_parameter_resolution_e3014(
    parameters: OneToOne[ParameterId, Parameter],
    resolutions: OneToOne[ParameterId, ParameterResolution],
) -> List[Diagnostic]:
    diagnostics: List[Diagnostic] = []

    for id, resolution in resolutions.items():
        if len(resolution.accepted) != 1:
            for _ in resolution.rejected:
                diagnostics.append(
                    report_parameter_resolution_e3014(parameters.get(id))
                )

    return diagnostics


def report_parameter_resolution_e3014(entry: Parameter) -> Diagnostic:
    return Diagnostic(
        ref=entry.ref,
        code="E3014",
        message=f"Invalid parameter {entry}, reason: unknown.",
    )
