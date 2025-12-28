from dataclasses import dataclass
from typing import Dict, Iterable, Tuple, TypeVar

from i13c import ast

AstNode = TypeVar("AstNode")


@dataclass(kw_only=True, frozen=True)
class NodeId:
    value: int


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

    def items(self) -> Iterable[Tuple[NodeId, AstNode]]:
        return self.id_to_node.items()

    def get_by_id(self, node_id: NodeId) -> AstNode:
        return self.id_to_node[node_id]

    def get_by_node(self, node: AstNode) -> NodeId:
        return self.node_to_id[node]


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


class NodesVisitor:
    def __init__(self) -> None:
        self.counter = 0
        self.nodes = Nodes.empty()

    def next(self) -> NodeId:
        self.counter += 1
        nid = NodeId(value=self.counter)

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
