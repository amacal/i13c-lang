from typing import Any, Dict

from i13c.core.dag import GraphGroup, GraphNode, Prefix
from i13c.semantic.model import (
    BasicNodes,
    CallGraph,
    IndexEdges,
    LiveComponents,
    SemanticGraph,
)
from i13c.semantic.nodes.analyses.callables import configure_callables_live
from i13c.semantic.nodes.analyses.callgraphs import configure_callgraphs_live
from i13c.semantic.nodes.analyses.controlflows import configure_flowgraphs_live
from i13c.semantic.nodes.entities.callsites import configure_callsites
from i13c.semantic.nodes.entities.expressions import configure_expressions
from i13c.semantic.nodes.entities.functions import configure_functions
from i13c.semantic.nodes.entities.instructions import configure_instructions
from i13c.semantic.nodes.entities.literals import configure_literals
from i13c.semantic.nodes.entities.operands import configure_operands
from i13c.semantic.nodes.entities.parameters import configure_parameters
from i13c.semantic.nodes.entities.snippets import configure_snippets
from i13c.semantic.nodes.indices.callgraphs import configure_callgraphs
from i13c.semantic.nodes.indices.controlflows import configure_flowgraph_by_function
from i13c.semantic.nodes.indices.dataflows import configure_dataflow_by_flownode
from i13c.semantic.nodes.indices.entrypoints import configure_entrypoint_by_callable
from i13c.semantic.nodes.indices.environments import configure_environment_by_flownode
from i13c.semantic.nodes.indices.instances import configure_instance_by_callsite
from i13c.semantic.nodes.indices.terminalities import configure_terminality_by_function
from i13c.semantic.nodes.indices.usages import configure_usages_by_expression
from i13c.semantic.nodes.indices.variables import configure_variables_by_parameters
from i13c.semantic.nodes.resolutions.callsites import configure_resolution_by_callsite
from i13c.semantic.nodes.resolutions.instructions import (
    configure_resolution_by_instruction,
)
from i13c.semantic.rules.e3000 import configure_e3000
from i13c.semantic.rules.e3001 import configure_e3001
from i13c.semantic.rules.e3002 import configure_e3002
from i13c.semantic.rules.e3003 import configure_e3003
from i13c.semantic.rules.e3004 import configure_e3004
from i13c.semantic.rules.e3005 import configure_e3005
from i13c.semantic.rules.e3006 import configure_e3006
from i13c.semantic.rules.e3007 import configure_e3007
from i13c.semantic.rules.e3008 import configure_e3008
from i13c.semantic.rules.e3010 import configure_e3010
from i13c.semantic.rules.e3011 import configure_e3011
from i13c.semantic.rules.e3012 import configure_e3012
from i13c.semantic.syntax import SyntaxGraph


def configure_semantic_graph() -> GraphGroup:
    nodes = GraphGroup(
        nodes=[
            configure_callables_live(),
            configure_callgraphs_live(),
            configure_callgraphs(),
            configure_callsites(),
            configure_dataflow_by_flownode(),
            configure_entrypoint_by_callable(),
            configure_environment_by_flownode(),
            configure_expressions(),
            configure_flowgraph_by_function(),
            configure_flowgraphs_live(),
            configure_functions(),
            configure_instance_by_callsite(),
            configure_instructions(),
            configure_literals(),
            configure_operands(),
            configure_parameters(),
            configure_resolution_by_callsite(),
            configure_resolution_by_instruction(),
            configure_snippets(),
            configure_terminality_by_function(),
            configure_usages_by_expression(),
            configure_variables_by_parameters(),
        ]
    )

    rules = GraphGroup(
        nodes=[
            configure_e3000(),
            configure_e3001(),
            configure_e3002(),
            configure_e3003(),
            configure_e3004(),
            configure_e3005(),
            configure_e3006(),
            configure_e3007(),
            configure_e3008(),
            configure_e3010(),
            configure_e3011(),
            configure_e3012(),
        ]
    )

    return GraphGroup(nodes=[nodes, rules, configure()])


def configure() -> GraphNode:
    return GraphNode(
        builder=build,
        produces=("semantic/graph",),
        requires=frozenset(
            {
                ("syntax", "syntax/graph"),
                ("entities", Prefix(value="entities/")),
                ("indices", Prefix(value="indices/")),
                ("resolutions", Prefix(value="resolutions/")),
                ("analyses", Prefix(value="analyses/")),
            }
        ),
    )


def build(
    syntax: SyntaxGraph,
    entities: Dict[str, Any],
    indices: Dict[str, Any],
    resolutions: Dict[str, Any],
    analyses: Dict[str, Any],
) -> SemanticGraph:
    return SemanticGraph(
        generator=syntax.generator,
        basic=BasicNodes(
            literals=entities["entities/literals"],
            operands=entities["entities/operands"],
            instructions=entities["entities/instructions"],
            expressions=entities["entities/expressions"],
            snippets=entities["entities/snippets"],
            functions=entities["entities/functions"],
            callsites=entities["entities/callsites"],
            parameters=entities["entities/parameters"],
            variables=entities["entities/variables"],
        ),
        indices=IndexEdges(
            terminality_by_function=indices["indices/terminality-by-function"],
            resolution_by_callsite=resolutions["resolutions/callsites"],
            resolution_by_instruction=resolutions["resolutions/instructions"],
            flowgraph_by_function=indices["indices/flowgraph-by-function"],
            instance_by_callsite=indices["indices/instance-by-callsite"],
            dataflow_by_flownode=indices["indices/dataflow-by-flownode"],
            variables_by_parameter=indices["indices/variables-by-parameter"],
            environment_by_flownode=indices["indices/environment-by-flownode"],
        ),
        callgraph=CallGraph(
            calls_by_caller=indices["indices/calls-by-caller"],
            calls_by_callee=indices["indices/calls-by-callee"],
        ),
        live=LiveComponents(
            entrypoints=indices["indices/entrypoints-by-callable"],
            flowgraph_by_function=analyses["analyses/flowgraph-by-function/live"],
        ),
        callable_live=analyses["analyses/callables/live"],
        callgraph_live=analyses["analyses/calls-by-caller/live"],
    )
