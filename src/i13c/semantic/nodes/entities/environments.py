from typing import Dict, List

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.environments import (
    Environment,
    EnvironmentId,
    EnvironmentTarget,
)
from i13c.semantic.typing.entities.labels import LabelId
from i13c.semantic.typing.entities.slots import SlotId
from i13c.syntax.tree.snippet import Label


def configure_environments() -> GraphNode:
    return GraphNode(
        builder=build_environments,
        constraint=None,
        produces=("entities/environments",),
        requires=frozenset({("graph", "syntax/graph")}),
    )


def build_environments(
    graph: SyntaxGraph,
) -> OneToOne[EnvironmentId, Environment]:
    environments: Dict[EnvironmentId, Environment] = {}

    for id, entry in graph.snippets.items():
        # derive environment ID from globally unique node ID
        environment_id = EnvironmentId(value=id.value)

        # a list of all the targets
        targets: List[EnvironmentTarget] = []

        # append all slots
        for slot in entry.signature.slots:
            nid = graph.slots.get_by_node(slot)
            targets.append(SlotId(value=nid.value))

        # append all labels
        for instr in entry.body:
            if isinstance(instr, Label):
                nid = graph.labels.get_by_node(instr)
                targets.append(LabelId(value=nid.value))

        environments[environment_id] = Environment(
            ref=entry.ref,
            kind="snippet",
            entries=targets,
        )

    return OneToOne[EnvironmentId, Environment].instance(environments)
