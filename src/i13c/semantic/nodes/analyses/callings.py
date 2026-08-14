from collections.abc import Iterable

from i13c.core.graph import GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.analyses.asmlets import Asmlet, AsmletId
from i13c.semantic.typing.analyses.callings import (
    Calling,
    CallingBinding,
    CallingClobber,
    CallingUnbound,
    CallSiteArgument,
)
from i13c.semantic.typing.entities.callsites import CallSiteId
from i13c.semantic.typing.resolutions.callsites import CallSiteAcceptance


def configure_callings() -> GraphNode:
    return GraphNode(
        builder=build_callings,
        constraint=None,
        produces=("analyses/callings",),
        requires=frozenset(
            {
                ("asmlets", "analyses/asmlets"),
                ("callsites", "resolutions/callsites/accepted"),
            }
        ),
        views=GraphViews(list=ListExtractor),
    )


def build_callings(
    asmlets: OneToOne[AsmletId, Asmlet],
    callsites: OneToOne[CallSiteId, CallSiteAcceptance],
) -> OneToOne[CallSiteId, Calling]:
    callings: dict[CallSiteId, Calling] = {}

    # fmt: off
    caller_saved = [b"rdi", b"rsi", b"rdx", b"rcx", b"r8", b"r9", b"rax", b"r10", b"r11"]
    callee_saved = [b"rbx", b"r12", b"r13", b"r14", b"r15", b"rbp"]
    # fmt: on

    # copy by default all available callsites
    for cid, entry in callsites.items():
        bindings: list[CallingBinding] = []
        clobbers: list[CallingClobber] = []
        unbounds: list[CallingUnbound] = []

        for idx, reg in enumerate(caller_saved):
            if idx < len(entry.signature.parameters):
                bindings.append(CallingBinding(name=reg))
            else:
                clobbers.append(CallingClobber(name=reg))

        for reg in callee_saved:
            unbounds.append(CallingUnbound(name=reg))

        callings[cid] = Calling(
            callsite=cid,
            ref=entry.ref,
            target=entry,
            signature=entry.signature,
            arguments=entry.arguments,
            parameters=entry.signature.parameters,
            bindings=bindings,
            clobbers=clobbers,
            unbounds=unbounds,
        )

    # override callings with available asmlet callsites
    for entry in asmlets.values():
        for callsite in entry.callsites:
            target = callings[callsite.id]

            # the callsite is not converted yet
            assert isinstance(target.target, CallSiteAcceptance)
            arguments = list(find_arguments(target.target, entry))

            target.target = entry
            target.signature = entry.signature
            target.arguments = arguments
            target.parameters = entry.parameters

            clobbers_tmp: list[bytes] = [clobber.name for clobber in entry.clobbers]
            bindings_tmp: list[bytes] = [binding.dst for binding in entry.bindings]

            target.clobbers = [
                CallingClobber(name=clobber) for clobber in clobbers_tmp
            ]

            target.bindings = [
                CallingBinding(name=binding) for binding in bindings_tmp
            ]

            target.unbounds = [
                CallingUnbound(name=reg) for reg in [*callee_saved, *caller_saved]
                if reg not in bindings_tmp and reg not in clobbers_tmp
            ]

    return OneToOne[CallSiteId, Calling].instance(callings)


def find_arguments(
    callsite: CallSiteAcceptance, asmlet: Asmlet
) -> Iterable[CallSiteArgument]:
    for arg, param in zip(callsite.arguments, callsite.signature.parameters):
        if param.name not in asmlet.keys:
            yield arg


class ListExtractor:
    def __init__(self, data: OneToOne[CallSiteId, Calling]):
        self.data = data

    def extract(self) -> Iterable[tuple[CallSiteId, Calling]]:
        yield from self.data.items()

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "callsite": "CallSite",
            "target": "Target",
            "arguments": "Arguments",
        }

    @staticmethod
    def rows(key: CallSiteId, entry: Calling) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "callsite": key.identify(1),
            "target": entry.target.id.identify(1),
            "arguments": ", ".join(str(arg) for arg in entry.arguments),
        }
