from dataclasses import dataclass
from typing import Dict, Iterable, Tuple, TypeVar

from i13c.core.dag import GraphGroup, GraphNode
from i13c.core.generator import Generator
from i13c.syntax import tree

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
    def __init__(self, generator: Generator) -> None:
        self.generator = generator
        self.graph = SyntaxGraph.empty()

    def next(self) -> NodeId:
        return NodeId(value=self.generator.next())

    def on_program(self, program: tree.Program) -> None:
        pass

    def on_snippet(self, snippet: tree.Snippet) -> None:
        self.graph.snippets.append(self.next(), snippet)

    def on_instruction(self, instruction: tree.Instruction) -> None:
        self.graph.instructions.append(self.next(), instruction)

    def on_function(self, function: tree.Function) -> None:
        self.graph.functions.append(self.next(), function)

    def on_parameter(self, parameter: tree.Parameter) -> None:
        self.graph.parameters.append(self.next(), parameter)

    def on_statement(self, statement: tree.Statement) -> None:
        self.graph.statements.append(self.next(), statement)

    def on_literal(self, literal: tree.Literal) -> None:
        self.graph.literals.append(self.next(), literal)

    def on_expression(self, expression: tree.Expression) -> None:
        self.graph.expressions.append(self.next(), expression)

    def on_operand(self, operand: tree.Operand) -> None:
        self.graph.operands.append(self.next(), operand)


@dataclass(kw_only=True)
class SyntaxGraph:
    snippets: Bidirectional[tree.Snippet]
    operands: Bidirectional[tree.Operand]
    instructions: Bidirectional[tree.Instruction]
    functions: Bidirectional[tree.Function]
    statements: Bidirectional[tree.Statement]
    literals: Bidirectional[tree.Literal]
    expressions: Bidirectional[tree.Expression]
    parameters: Bidirectional[tree.Parameter]

    @staticmethod
    def empty() -> SyntaxGraph:
        return SyntaxGraph(
            snippets=Bidirectional[tree.Snippet].empty(),
            operands=Bidirectional[tree.Operand].empty(),
            instructions=Bidirectional[tree.Instruction].empty(),
            functions=Bidirectional[tree.Function].empty(),
            statements=Bidirectional[tree.Statement].empty(),
            literals=Bidirectional[tree.Literal].empty(),
            expressions=Bidirectional[tree.Expression].empty(),
            parameters=Bidirectional[tree.Parameter].empty(),
        )


def build_syntax_graph(
    generator: Generator,
    program: tree.Program,
) -> SyntaxGraph:
    visitor = NodesVisitor(generator)
    program.accept(visitor)

    return visitor.graph


def configure_syntax_graph() -> GraphGroup:
    def produce(generator: Generator, program: tree.Program) -> SyntaxGraph:
        return build_syntax_graph(generator, program)

    node = GraphNode(
        builder=produce,
        constraint=None,
        produces=("syntax/graph",),
        requires=frozenset(
            {
                ("generator", "core/generator"),
                ("program", "ast/program"),
            }
        ),
    )

    return GraphGroup(nodes=[node])
