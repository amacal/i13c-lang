from typing import Dict, List, Literal, Union

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToMany, OneToOne
from i13c.semantic.typing.entities.cflows import FlowEntry, FlowExit, FlowMember
from i13c.semantic.typing.entities.cpaths import ControlPaths
from i13c.semantic.typing.entities.flags import FlagsId
from i13c.semantic.typing.entities.noreturns import NoReturn
from i13c.semantic.typing.entities.signatures import SignatureId
from i13c.semantic.typing.entities.snippets import Snippet, SnippetId
from i13c.semantic.typing.entities.statements import StatementId
from i13c.semantic.typing.resolutions.callsites import CallSiteAcceptance
from i13c.semantic.typing.resolutions.flags import FlagsAcceptance
from i13c.semantic.typing.resolutions.signatures import SignatureAcceptance


def configure_noreturns() -> GraphNode:
    return GraphNode(
        builder=build_noreturns,
        constraint=None,
        produces=("entities/noreturns",),
        requires=frozenset(
            {
                ("flags", "resolutions/flags/accepted"),
                ("snippets", "entities/snippets"),
                ("cpaths", "indices/cpaths/signatures"),
                ("signatures", "resolutions/signatures/accepted"),
                ("callsites", "indices/callsites/statements"),
            }
        ),
    )


def build_noreturns(
    flags: OneToOne[FlagsId, FlagsAcceptance],
    snippets: OneToOne[SnippetId, Snippet],
    cpaths: OneToOne[SignatureId, ControlPaths],
    signatures: OneToOne[SignatureId, SignatureAcceptance],
    callsites: OneToMany[StatementId, CallSiteAcceptance],
) -> OneToOne[SignatureId, NoReturn]:
    noreturns: Dict[SignatureId, NoReturn] = {}

    # seed noreturn from all snippets
    for entry in snippets.values():
        noreturn = False

        if entry.flags is not None:
            noreturn = flags.get(entry.flags).noreturn

        noreturns[entry.signature] = NoReturn(
            signature=signatures.get(entry.signature),
            path=[],
            outcome=noreturn,
        )

    changed = True
    while changed:
        changed = False

        for sig, entry in cpaths.items():

            # skip already processed signatures
            if sig in noreturns:
                continue

            noreturn = is_function_noreturn(noreturns, callsites, entry)
            changed = changed or noreturn is not None

            if noreturn is not None:
                signature = signatures.get(sig)
                outcome = True if isinstance(noreturn, NoReturn) else False

                path = (
                    [noreturn.signature]
                    if isinstance(noreturn, NoReturn) and not noreturn.path
                    else []
                )

                noreturns[sig] = NoReturn(
                    signature=signature,
                    path=[signature] + path if isinstance(noreturn, NoReturn) else [],
                    outcome=outcome,
                )

    return OneToOne[SignatureId, NoReturn].instance(noreturns)


def is_function_noreturn(
    noreturns: Dict[SignatureId, NoReturn],
    callsites: OneToMany[StatementId, CallSiteAcceptance],
    target: ControlPaths,
) -> Union[NoReturn, None, Literal[False]]:
    noreturn: Union[NoReturn, None, Literal[False]] = None

    # if any path is returning, the function is returning
    for idx in range(len(target.paths)):
        noreturn = is_path_noreturn(
            noreturns,
            callsites,
            target.paths[idx],
            target.flows.source.nodes,
        )

        if noreturn is False:
            return False

        if noreturn is None:
            return None

    assert isinstance(noreturn, NoReturn)
    return noreturn


def is_path_noreturn(
    noreturns: Dict[SignatureId, NoReturn],
    callsites: OneToMany[StatementId, CallSiteAcceptance],
    paths: List[int],
    nodes: List[FlowMember],
) -> Union[NoReturn, None, Literal[False]]:
    for node in paths:
        node = nodes[node]

        # if we encounter a flow exit, the path is returning
        if isinstance(node, FlowExit):
            return False

        if isinstance(node, FlowEntry):
            continue

        for callsite in callsites.find(node.target):
            noreturn = noreturns.get(callsite.signature.id)

            # if the callee is already known to be not returning, we can report the path as not returning
            if noreturn is not None and noreturn.outcome:
                return noreturn

            # if the callee is not recognized yet, we cannot make a decision about the path
            elif noreturn is None:
                return None

    # all paths are returning, so we can report the path as returning
    return False
