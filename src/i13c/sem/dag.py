from collections import defaultdict
from typing import Any, Dict, List, Set

from i13c.sem.infra import Configuration
from i13c.sem.nodes.analyses.callables import configure_callables_live
from i13c.sem.nodes.analyses.callgraphs import configure_callgraphs_live
from i13c.sem.nodes.analyses.controlflows import configure_flowgraphs_live
from i13c.sem.nodes.entities.callsites import configure_callsites
from i13c.sem.nodes.entities.expressions import configure_expressions
from i13c.sem.nodes.entities.functions import configure_functions
from i13c.sem.nodes.entities.instructions import configure_instructions
from i13c.sem.nodes.entities.literals import configure_literals
from i13c.sem.nodes.entities.operands import configure_operands
from i13c.sem.nodes.entities.parameters import configure_parameters
from i13c.sem.nodes.entities.snippets import configure_snippets
from i13c.sem.nodes.indices.callgraphs import configure_callgraphs
from i13c.sem.nodes.indices.controlflows import configure_flowgraph_by_function
from i13c.sem.nodes.indices.dataflows import configure_dataflow_by_flownode
from i13c.sem.nodes.indices.entrypoints import configure_entrypoint_by_callable
from i13c.sem.nodes.indices.instances import configure_instance_by_callsite
from i13c.sem.nodes.indices.terminalities import configure_terminality_by_function
from i13c.sem.nodes.indices.variables import configure_variables_by_parameters
from i13c.sem.nodes.resolutions.callsites import configure_resolution_by_callsite
from i13c.sem.nodes.resolutions.instructions import configure_resolution_by_instruction
from i13c.sem.syntax import SyntaxGraph


def reorder_configurations(configs: List[Configuration]) -> List[Configuration]:
    # build producer map
    producer: Dict[str, Configuration] = {}

    for cfg in configs:
        for p in cfg.produces:
            producer[p] = cfg

    # build dependency graph
    edges: Dict[Configuration, Set[Configuration]] = defaultdict(set)
    indeg: Dict[Configuration, int] = {c: 0 for c in configs}

    for cfg in configs:
        for _, req in cfg.requires:
            dep = producer[req]
            edges[dep].add(cfg)
            indeg[cfg] += 1

    # topological sorting
    queue = [c for c in configs if indeg[c] == 0]
    out: List[Configuration] = []

    while queue:
        c = queue.pop()
        out.append(c)

        for nxt in edges[c]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                queue.append(nxt)

    return out


def configure_semantic_model(graph: SyntaxGraph) -> Dict[str, Any]:
    def build() -> SyntaxGraph:
        return graph

    syntax = Configuration(
        builder=build,
        produces=("syntax/graph",),
        requires=frozenset(),
    )

    configs: List[Configuration] = [
        syntax,
        configure_callgraphs(),
        configure_callsites(),
        configure_expressions(),
        configure_functions(),
        configure_instructions(),
        configure_literals(),
        configure_operands(),
        configure_parameters(),
        configure_snippets(),
        configure_dataflow_by_flownode(),
        configure_entrypoint_by_callable(),
        configure_flowgraph_by_function(),
        configure_instance_by_callsite(),
        configure_resolution_by_callsite(),
        configure_resolution_by_instruction(),
        configure_terminality_by_function(),
        configure_variables_by_parameters(),
        configure_callables_live(),
        configure_callgraphs_live(),
        configure_flowgraphs_live(),
    ]

    artifacts: Dict[str, Any] = {}

    for cfg in reorder_configurations(configs):
        # prepare arguments
        args = {name: artifacts[req] for name, req in cfg.requires}

        # build dataset
        dataset = cfg.builder(**args)

        # store single artifact
        for producer in cfg.produces:
            artifacts[producer] = dataset

        # store multiple artifacts
        if len(cfg.produces) > 1:
            for idx, producer in enumerate(cfg.produces):
                artifacts[producer] = dataset[idx]

    return artifacts
