from typing import Dict, List

from i13c.core.generator import Generator
from i13c.core.mapping import OneToOne
from i13c.sem.infra import Configuration
from i13c.sem.syntax import SyntaxGraph
from i13c.sem.typing.entities.functions import Function, FunctionId
from i13c.sem.typing.indices.controlflows import (
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
        edges: Dict[FlowNode, List[FlowNode]] = {}

        if not function.statements:
            edges[entry] = [exit]

        else:

            stmts = function.statements
            edges[entry] = [stmts[0]]

            for predecessor, successor in zip(stmts, stmts[1:]):
                edges[predecessor] = [successor]

            edges[stmts[-1]] = [exit]

        flowgraphs[fid] = FlowGraph(
            entry=entry,
            exit=exit,
            edges=edges,
        )

    return OneToOne[FunctionId, FlowGraph].instance(flowgraphs)
