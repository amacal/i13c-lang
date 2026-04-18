from typing import Dict

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.callsites import CallSiteId
from i13c.semantic.typing.entities.instructions import Instruction, InstructionId
from i13c.semantic.typing.entities.literals import Literal, LiteralId
from i13c.semantic.typing.entities.operands import Operand, OperandId
from i13c.semantic.typing.entities.snippets import Snippet, SnippetId
from i13c.semantic.typing.indices.instances import Instance
from i13c.semantic.typing.resolutions.callsites import (
    CallSiteResolution,
)
from i13c.semantic.typing.resolutions.instructions import (
    InstructionResolution,
)


def configure_instance_by_callsite() -> GraphNode:
    return GraphNode(
        builder=build_instances,
        constraint=None,
        produces=("indices/instance-by-callsite",),
        requires=frozenset(
            {
                ("snippets", "entities/snippets"),
                ("literals", "entities/literals"),
                ("operands", "entities/operands"),
                ("instructions", "entities/instructions"),
                ("callsites_resolutions", "resolutions/callsites"),
                ("instructions_resolutions", "resolutions/instructions"),
            }
        ),
    )


def build_instances(
    snippets: OneToOne[SnippetId, Snippet],
    literals: OneToOne[LiteralId, Literal],
    operands: OneToOne[OperandId, Operand],
    instructions: OneToOne[InstructionId, Instruction],
    callsites_resolutions: OneToOne[CallSiteId, CallSiteResolution],
    instructions_resolutions: OneToOne[InstructionId, InstructionResolution],
) -> OneToOne[CallSiteId, Instance]:
    instances: Dict[CallSiteId, Instance] = {}

    return OneToOne[CallSiteId, Instance].instance(instances)
