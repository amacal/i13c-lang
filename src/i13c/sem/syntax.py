from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Tuple, TypeVar

from i13c import ast


@dataclass(kw_only=True, frozen=True)
class NodeId:
    value: int


AstNode = TypeVar("AstNode")


@dataclass(kw_only=True)
class Bidirectional[AstNode]:
    node_to_id: Dict[AstNode, NodeId]
    id_to_node: Dict[NodeId, AstNode]

    @staticmethod
    def empty() -> Bidirectional[AstNode]:
        return Bidirectional(node_to_id={}, id_to_node={})

    def append(self, id: NodeId, node: AstNode) -> None:
        self.node_to_id[node] = id
        self.id_to_node[id] = node

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


@dataclass(kw_only=True)
class Nodes:
    snippets: Bidirectional[ast.Snippet]
    instructions: Bidirectional[ast.Instruction]
    functions: Bidirectional[ast.Function]
    statements: Bidirectional[ast.Statement]
    literals: Bidirectional[ast.Literal]

    @staticmethod
    def empty() -> "Nodes":
        return Nodes(
            snippets=Bidirectional[ast.Snippet].empty(),
            instructions=Bidirectional[ast.Instruction].empty(),
            functions=Bidirectional[ast.Function].empty(),
            statements=Bidirectional[ast.Statement].empty(),
            literals=Bidirectional[ast.Literal].empty(),
        )


@dataclass(kw_only=True)
class Edges:
    pass


class NodesVisitor:
    def __init__(self) -> None:
        self.counter = 0
        self.nodes = Nodes.empty()

    def next(self) -> NodeId:
        nid = NodeId(value=self.counter)
        self.counter += 1
        return nid

    def on_program(self, program: ast.Program) -> None:
        pass

    def on_snippet(self, snippet: ast.Snippet) -> None:
        self.nodes.snippets.append(self.next(), snippet)

    def on_instruction(self, instruction: ast.Instruction) -> None:
        self.nodes.instructions.append(self.next(), instruction)

    def on_function(self, function: ast.Function) -> None:
        self.nodes.functions.append(self.next(), function)

    def on_statement(self, statement: ast.Statement) -> None:
        self.nodes.statements.append(self.next(), statement)

    def on_literal(self, literal: ast.Literal) -> None:
        self.nodes.literals.append(self.next(), literal)


@dataclass(kw_only=True)
class SyntaxGraph:
    nodes: Nodes


def build_syntax_graph(program: ast.Program) -> SyntaxGraph:
    visitor = NodesVisitor()
    program.accept(visitor)

    return SyntaxGraph(nodes=visitor.nodes)
