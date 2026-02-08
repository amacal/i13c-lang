from dataclasses import dataclass
from typing import Any, Dict, List, Set

from i13c.core.generator import Generator
from i13c.core.mapping import OneToMany, OneToOne
from i13c.semantic.dag import configure_semantic_model
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.callables import CallableTarget
from i13c.semantic.typing.entities.callsites import CallSite, CallSiteId
from i13c.semantic.typing.entities.expressions import Expression, ExpressionId
from i13c.semantic.typing.entities.functions import Function, FunctionId
from i13c.semantic.typing.entities.instructions import Instruction, InstructionId
from i13c.semantic.typing.entities.literals import Literal, LiteralId
from i13c.semantic.typing.entities.operands import Operand, OperandId
from i13c.semantic.typing.entities.parameters import Parameter, ParameterId
from i13c.semantic.typing.entities.snippets import Snippet, SnippetId
from i13c.semantic.typing.indices.callgraphs import CallPair
from i13c.semantic.typing.indices.controlflows import FlowGraph, FlowNode
from i13c.semantic.typing.indices.dataflows import DataFlow
from i13c.semantic.typing.indices.entrypoints import EntryPoint
from i13c.semantic.typing.indices.environments import Environment
from i13c.semantic.typing.indices.instances import Instance
from i13c.semantic.typing.indices.terminalities import Terminality
from i13c.semantic.typing.indices.variables import Variable, VariableId
from i13c.semantic.typing.resolutions.callsites import CallSiteResolution
from i13c.semantic.typing.resolutions.instructions import InstructionResolution


@dataclass
class BasicNodes:
    literals: OneToOne[LiteralId, Literal]
    operands: OneToOne[OperandId, Operand]
    instructions: OneToOne[InstructionId, Instruction]
    expressions: OneToOne[ExpressionId, Expression]
    snippets: OneToOne[SnippetId, Snippet]
    functions: OneToOne[FunctionId, Function]
    callsites: OneToOne[CallSiteId, CallSite]
    parameters: OneToOne[ParameterId, Parameter]
    variables: OneToOne[VariableId, Variable]


@dataclass
class IndexEdges:
    terminality_by_function: OneToOne[FunctionId, Terminality]
    resolution_by_callsite: OneToOne[CallSiteId, CallSiteResolution]
    resolution_by_instruction: OneToOne[InstructionId, InstructionResolution]
    flowgraph_by_function: OneToOne[FunctionId, FlowGraph]
    dataflow_by_flownode: OneToOne[FlowNode, DataFlow]
    instance_by_callsite: OneToOne[CallSiteId, Instance]
    variables_by_parameter: OneToOne[ParameterId, VariableId]
    environment_by_flownode: OneToOne[FlowNode, Environment]


@dataclass
class LiveComponents:
    entrypoints: OneToOne[CallableTarget, EntryPoint]
    flowgraph_by_function: OneToOne[FunctionId, FlowGraph]


@dataclass
class CallGraph:
    calls_by_caller: OneToMany[CallableTarget, CallPair]
    calls_by_callee: OneToMany[CallableTarget, CallPair]


@dataclass(kw_only=True)
class SemanticGraph:
    generator: Generator

    callgraph_live: Dict[CallableTarget, List[CallPair]]
    callable_live: Set[CallableTarget]

    basic: BasicNodes
    indices: IndexEdges
    callgraph: CallGraph
    live: LiveComponents


def build_semantic_graph(graph: SyntaxGraph) -> SemanticGraph:
    artifacts: Dict[str, Any] = configure_semantic_model(graph)

    return SemanticGraph(
        generator=graph.generator,
        basic=BasicNodes(
            literals=artifacts["entities/literals"],
            operands=artifacts["entities/operands"],
            instructions=artifacts["entities/instructions"],
            expressions=artifacts["entities/expressions"],
            snippets=artifacts["entities/snippets"],
            functions=artifacts["entities/functions"],
            callsites=artifacts["entities/callsites"],
            parameters=artifacts["entities/parameters"],
            variables=artifacts["entities/variables"],
        ),
        indices=IndexEdges(
            terminality_by_function=artifacts["indices/terminality-by-function"],
            resolution_by_callsite=artifacts["resolutions/callsites"],
            resolution_by_instruction=artifacts["resolutions/instructions"],
            flowgraph_by_function=artifacts["indices/flowgraph-by-function"],
            instance_by_callsite=artifacts["indices/instance-by-callsite"],
            dataflow_by_flownode=artifacts["indices/dataflow-by-flownode"],
            variables_by_parameter=artifacts["indices/variables-by-parameter"],
            environment_by_flownode=artifacts["indices/environment-by-flownode"],
        ),
        callgraph=CallGraph(
            calls_by_caller=artifacts["indices/calls-by-caller"],
            calls_by_callee=artifacts["indices/calls-by-callee"],
        ),
        live=LiveComponents(
            entrypoints=artifacts["indices/entrypoints-by-callable"],
            flowgraph_by_function=artifacts["analyses/flowgraph-by-function/live"],
        ),
        callable_live=artifacts["analyses/callables/live"],
        callgraph_live=artifacts["analyses/calls-by-caller/live"],
    )
