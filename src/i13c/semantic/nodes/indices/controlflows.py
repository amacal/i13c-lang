from typing import Dict, List

from i13c.core.generator import Generator
from i13c.core.mapping import OneToOne
from i13c.semantic.infra import Configuration
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.functions import Function, FunctionId
from i13c.semantic.typing.indices.controlflows import (
    FlowEntry,
    FlowExit,
    FlowGraph,
    FlowNode,
)


def configure_flowgraph_by_function() -> Configuration:
    return Configuration(
        builder=build_flowgraphs,
        produces=("indices/flowgraph-by-function",),
        requires=frozenset(
            {
                ("graph", "syntax/graph"),
                ("functions", "entities/functions"),
            }
        ),
    )


def build_flowgraphs(
    graph: SyntaxGraph,
    functions: OneToOne[FunctionId, Function],
) -> OneToOne[FunctionId, FlowGraph]:

    generator: Generator = graph.generator
    flowgraphs: Dict[FunctionId, FlowGraph] = {}

    for fid, function in functions.items():
        entry = FlowEntry(value=generator.next())
        exit = FlowExit(value=generator.next())

        forward: Dict[FlowNode, List[FlowNode]] = {}
        backward: Dict[FlowNode, List[FlowNode]] = {}

        if not function.statements:
            forward[entry] = [exit]
            backward[exit] = [entry]

        else:

            stmts = function.statements

            forward[entry] = [stmts[0]]
            backward[stmts[0]] = [entry]

            for predecessor, successor in zip(stmts, stmts[1:]):
                forward[predecessor] = [successor]
                backward[successor] = [predecessor]

            forward[stmts[-1]] = [exit]
            backward[exit] = [stmts[-1]]

        flowgraphs[fid] = FlowGraph(
            entry=entry,
            exit=exit,
            forward=forward,
            backward=backward,
        )

    return OneToOne[FunctionId, FlowGraph].instance(flowgraphs)
