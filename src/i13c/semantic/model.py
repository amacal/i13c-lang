from dataclasses import dataclass
from typing import Dict, List, Optional, Set

from i13c.core.mapping import OneToMany, OneToOne
from i13c.semantic.typing.entities import EntityNodes
from i13c.semantic.typing.entities.callables import CallableTarget
from i13c.semantic.typing.entities.callsites import CallSiteId
from i13c.semantic.typing.entities.expressions import ExpressionId
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.entities.instructions import InstructionId
from i13c.semantic.typing.entities.values import ValueId
from i13c.semantic.typing.indices.callgraphs import CallPair
from i13c.semantic.typing.indices.controlflows import FlowGraph, FlowNode
from i13c.semantic.typing.indices.dataflows import DataFlow
from i13c.semantic.typing.indices.entrypoints import EntryPoint
from i13c.semantic.typing.indices.environments import Environment
from i13c.semantic.typing.indices.instances import Instance
from i13c.semantic.typing.indices.terminalities import Terminality
from i13c.semantic.typing.indices.usages import UsageId
from i13c.semantic.typing.indices.variables import VariableId, VariableSource
from i13c.semantic.typing.resolutions import ResolutionNodes
from i13c.semantic.typing.resolutions.callsites import CallSiteResolution
from i13c.semantic.typing.resolutions.instructions import InstructionResolution
from i13c.semantic.typing.resolutions.values import ValueResolution


@dataclass
class IndexEdges:
    dataflow_by_flownode: OneToOne[FlowNode, DataFlow]
    environment_by_flownode: OneToOne[FlowNode, Environment]
    flowgraph_by_function: OneToOne[FunctionId, FlowGraph]
    instance_by_callsite: OneToOne[CallSiteId, Instance]
    resolution_by_callsite: OneToOne[CallSiteId, CallSiteResolution]
    resolution_by_instruction: OneToOne[InstructionId, InstructionResolution]
    resolution_by_value: OneToOne[ValueId, ValueResolution]
    terminality_by_function: OneToOne[FunctionId, Terminality]
    usages_by_expression: OneToMany[ExpressionId, UsageId]
    variables_by_parameter: OneToOne[VariableSource, VariableId]


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
    callgraph_live: Dict[CallableTarget, List[CallPair]]
    callable_live: Set[CallableTarget]

    entities: EntityNodes
    indices: IndexEdges
    callgraph: CallGraph
    live: LiveComponents
    resolutions: ResolutionNodes

    def find_function_by_name(self, name: bytes) -> Optional[FunctionId]:
        for fid, function in self.entities.functions.items():
            if function.identifier.data == name:
                return fid

        return None
