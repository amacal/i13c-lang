from dataclasses import dataclass
from typing import Dict, Iterable, Tuple, TypeVar

from i13c import ast
from i13c.core.dag import GraphGroup, GraphNode
from i13c.core.generator import Generator

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


class NodesVisitor:
    def __init__(self) -> None:
        self.generator = Generator()
        self.graph = SyntaxGraph.empty(self.generator)

    def next(self) -> NodeId:
        return NodeId(value=self.generator.next())

    def on_program(self, program: ast.Program) -> None:
        pass

    def on_snippet(self, snippet: ast.Snippet) -> None:
        self.graph.snippets.append(self.next(), snippet)

    def on_instruction(self, instruction: ast.Instruction) -> None:
        self.graph.instructions.append(self.next(), instruction)

    def on_function(self, function: ast.Function) -> None:
        self.graph.functions.append(self.next(), function)

    def on_parameter(self, parameter: ast.Parameter) -> None:
        self.graph.parameters.append(self.next(), parameter)

    def on_statement(self, statement: ast.Statement) -> None:
        self.graph.statements.append(self.next(), statement)

    def on_literal(self, literal: ast.Literal) -> None:
        self.graph.literals.append(self.next(), literal)

    def on_expression(self, expression: ast.Expression) -> None:
        self.graph.expressions.append(self.next(), expression)

    def on_operand(self, operand: ast.Operand) -> None:
        self.graph.operands.append(self.next(), operand)


@dataclass(kw_only=True)
class SyntaxGraph:
    generator: Generator
    snippets: Bidirectional[ast.Snippet]
    operands: Bidirectional[ast.Operand]
    instructions: Bidirectional[ast.Instruction]
    functions: Bidirectional[ast.Function]
    statements: Bidirectional[ast.Statement]
    literals: Bidirectional[ast.Literal]
    expressions: Bidirectional[ast.Expression]
    parameters: Bidirectional[ast.Parameter]

    @staticmethod
    def empty(generator: Generator) -> SyntaxGraph:
        return SyntaxGraph(
            generator=generator,
            snippets=Bidirectional[ast.Snippet].empty(),
            operands=Bidirectional[ast.Operand].empty(),
            instructions=Bidirectional[ast.Instruction].empty(),
            functions=Bidirectional[ast.Function].empty(),
            statements=Bidirectional[ast.Statement].empty(),
            literals=Bidirectional[ast.Literal].empty(),
            expressions=Bidirectional[ast.Expression].empty(),
            parameters=Bidirectional[ast.Parameter].empty(),
        )

    def next(self) -> int:
        return self.generator.next()


def build_syntax_graph(program: ast.Program) -> SyntaxGraph:
    visitor = NodesVisitor()
    program.accept(visitor)

    return visitor.graph


def configure_syntax_graph() -> GraphGroup:
    def produce(program: ast.Program) -> SyntaxGraph:
        return build_syntax_graph(program)

    node = GraphNode(
        builder=produce,
        produces=("syntax/graph",),
        requires=frozenset({("program", "ast/program")}),
    )

    return GraphGroup(nodes=[node])
