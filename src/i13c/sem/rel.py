from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Tuple, TypeVar

from i13c import ast

AstNode = TypeVar("AstNode")
NodeId = TypeVar("NodeId")


@dataclass(kw_only=True)
class Bidirectional[AstNode, NodeId]:
    node_to_id: Dict[AstNode, NodeId]
    id_to_node: Dict[NodeId, AstNode]
    attr_to_id: Dict[str, Dict[Any, NodeId]]

    def ids(self) -> Iterable[NodeId]:
        return self.id_to_node.keys()

    def values(self) -> Iterable[AstNode]:
        return self.node_to_id.keys()

    def items(self) -> Iterable[Tuple[NodeId, AstNode]]:
        return self.id_to_node.items()

    def get_by_id(self, node_id: NodeId) -> AstNode:
        return self.id_to_node[node_id]

    def get_by_ids(self, node_ids: List[NodeId]) -> List[AstNode]:
        return [self.id_to_node[nid] for nid in node_ids]

    def find_by_id(self, node_id: NodeId) -> Optional[AstNode]:
        return self.id_to_node.get(node_id)

    def find_by_ids(self, node_ids: List[NodeId]) -> List[AstNode]:
        return [self.id_to_node[nid] for nid in node_ids if nid in self.id_to_node]

    def find_by_node(self, node: AstNode) -> Optional[NodeId]:
        return self.node_to_id.get(node)

    def find_by_attr(self, attr: str, value: Any) -> Optional[NodeId]:
        return self.attr_to_id[attr].get(value)

    def get_by_node(self, node: AstNode) -> NodeId:
        return self.node_to_id[node]


LeftId = TypeVar("LeftId")
RightId = TypeVar("RightId")


@dataclass(kw_only=True)
class OneToMany[LeftId, RightId]:
    map: Dict[LeftId, List[RightId]]

    def items(self) -> Iterable[Tuple[LeftId, List[RightId]]]:
        return self.map.items()

    def get(self, left_id: LeftId) -> List[RightId]:
        return self.map.get(left_id, [])


@dataclass(kw_only=True)
class OneToOne[LeftId, RightId]:
    map: Dict[LeftId, RightId]

    def keys(self) -> Iterable[LeftId]:
        return self.map.keys()

    def items(self) -> Iterable[Tuple[LeftId, RightId]]:
        return self.map.items()

    def find_by_id(self, left_id: LeftId) -> Optional[RightId]:
        return self.map.get(left_id)


@dataclass(kw_only=True, frozen=True)
class FunctionId:
    value: int


@dataclass(kw_only=True, frozen=True)
class InstructionId:
    value: int


@dataclass(kw_only=True, frozen=True)
class ParameterId:
    value: int


@dataclass(kw_only=True, frozen=True)
class LiteralId:
    value: int


@dataclass(kw_only=True, frozen=True)
class CallId:
    value: int


@dataclass(kw_only=True, frozen=True)
class StatementId:
    value: int


@dataclass(kw_only=True, frozen=True)
class ArgumentId:
    value: int


@dataclass(kw_only=True)
class Nodes:
    functions: Bidirectional[ast.Function, FunctionId]
    instructions: Bidirectional[ast.Instruction, InstructionId]
    statements: Bidirectional[ast.Statement, StatementId]
    parameters: Bidirectional[ast.Parameter, ParameterId]
    arguments: Bidirectional[ast.Argument, ArgumentId]
    literals: Bidirectional[ast.Literal, LiteralId]
    calls: Bidirectional[ast.CallStatement, CallId]


@dataclass(kw_only=True)
class Edges:
    function_parameters: OneToMany[FunctionId, ParameterId]
    function_clobbers: OneToMany[FunctionId, ast.Register]
    parameter_bindings: OneToOne[ParameterId, ast.Register]
    call_targets: OneToOne[CallId, FunctionId]
    call_arguments: OneToMany[CallId, ArgumentId]
    statement_calls: OneToOne[StatementId, CallId]


@dataclass(kw_only=True)
class Type:
    name: bytes


@dataclass(kw_only=True)
class Analysis:
    is_terminal: OneToOne[FunctionId, bool]
    function_exits: OneToMany[FunctionId, StatementId]
    argument_types: OneToOne[ArgumentId, Type]
    parameter_types: OneToOne[ParameterId, Type]


@dataclass(kw_only=True)
class Relationships:
    nodes: Nodes
    edges: Edges
    analysis: Analysis
