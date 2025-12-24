from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Tuple, TypeVar

AstNode = TypeVar("AstNode")
NodeId = TypeVar("NodeId")


@dataclass(kw_only=True)
class Bidirectional[AstNode, NodeId]:
    node_to_id: Dict[AstNode, NodeId]
    id_to_node: Dict[NodeId, AstNode]

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

    def get_by_node(self, node: AstNode) -> NodeId:
        return self.node_to_id[node]

    def get_by_nodes(self, nodes: Iterable[AstNode]) -> List[NodeId]:
        return [self.node_to_id[node] for node in nodes]


LeftId = TypeVar("LeftId")
RightId = TypeVar("RightId")


@dataclass(kw_only=True)
class OneToMany[LeftId, RightId]:
    map: Dict[LeftId, List[RightId]]

    def keys(self) -> Iterable[LeftId]:
        return self.map.keys()

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
