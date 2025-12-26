from dataclasses import dataclass

from i13c import ast
from i13c.sem.core import Bidirectional


@dataclass(kw_only=True, frozen=True)
class NodeId:
    value: int


@dataclass(kw_only=True)
class Nodes:
    snippets: Bidirectional[ast.Snippet, NodeId]
    instructions: Bidirectional[ast.Instruction, NodeId]
    functions: Bidirectional[ast.Function, NodeId]
    statements: Bidirectional[ast.Statement, NodeId]
    literals: Bidirectional[ast.Literal, NodeId]

    @staticmethod
    def empty() -> "Nodes":
        return Nodes(
            snippets=Bidirectional[ast.Snippet, NodeId].empty(),
            instructions=Bidirectional[ast.Instruction, NodeId].empty(),
            functions=Bidirectional[ast.Function, NodeId].empty(),
            statements=Bidirectional[ast.Statement, NodeId].empty(),
            literals=Bidirectional[ast.Literal, NodeId].empty(),
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
