from typing import Dict

from i13c.core.generator import Generator
from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.analyses.asmlets import Asmlet, AsmletId
from i13c.semantic.typing.analyses.callings import Calling, CallingBinding, CallingId


def configure_callings() -> GraphNode:
    return GraphNode(
        builder=build_callings,
        constraint=None,
        produces=("analyses/callings",),
        requires=frozenset(
            {
                ("generator", "core/generator"),
                ("asmlets", "analyses/asmlets"),
            }
        ),
    )


def build_callings(
    generator: Generator,
    asmlets: OneToOne[AsmletId, Asmlet],
) -> OneToOne[CallingId, Calling]:
    callings: Dict[CallingId, Calling] = {}

    for entry in asmlets.values():
        cid = CallingId(value=generator.next())
        bindings = [
            CallingBinding(
                idx=param,
                register=dst,
            )
            for param, dst in entry.bindings
        ]

        callings[cid] = Calling(
            id=cid,
            ref=entry.ref,
            target=entry,
            bindings=bindings,
            callsites=entry.callsites,
        )

    return OneToOne[CallingId, Calling].instance(callings)
