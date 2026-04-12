from dataclasses import dataclass
from typing import Dict, Iterable, Tuple, TypeVar

from i13c.core.generator import Generator
from i13c.core.graph import GraphGroup, GraphNode
from i13c.syntax import tree
from i13c.syntax.tree.core import Path

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

    def on_program(self, program: tree.Program, path: Path) -> None:
        pass

    def on_snippet(self, snippet: tree.snippet.Snippet, path: Path) -> None:
        self.graph.snippets.append(self.next(), snippet)

    def on_signature(self, signature: tree.snippet.Signature, path: Path) -> None:
        self.graph.signatures.append(self.next(), signature)

    def on_slot(self, slot: tree.snippet.Slot, path: Path) -> None:
        self.graph.slots.append(self.next(), slot)

    def on_bind(self, bind: tree.snippet.Bind, path: Path) -> None:
        self.graph.binds.append(self.next(), bind)

    def on_label(self, label: tree.snippet.Label, path: Path) -> None:
        self.graph.labels.append(self.next(), label)

    def on_instruction(self, instruction: tree.snippet.Instruction, path: Path) -> None:
        self.graph.instructions.append(self.next(), instruction)

    def on_operand(self, operand: tree.snippet.Operand, path: Path) -> None:
        self.graph.operands.append(self.next(), operand)

    def on_immediate(self, immediate: tree.snippet.Immediate, path: Path) -> None:
        self.graph.immediates.append(self.next(), immediate)

    def on_register(self, register: tree.snippet.Register, path: Path) -> None:
        self.graph.registers.append(self.next(), register)

    def on_reference(self, reference: tree.snippet.Reference, path: Path) -> None:
        self.graph.references.append(self.next(), reference)

    def on_function(self, function: tree.function.Function, path: Path) -> None:
        self.graph.functions.append(self.next(), function)

    def on_parameter(self, parameter: tree.function.Parameter, path: Path) -> None:
        self.graph.parameters.append(self.next(), parameter)

    def on_statement(self, statement: tree.function.Statement, path: Path) -> None:
        self.graph.statements.append(self.next(), statement)

    def on_literal(self, literal: tree.function.Literal, path: Path) -> None:
        self.graph.literals.append(self.next(), literal)

    def on_expression(self, expression: tree.function.Expression, path: Path) -> None:
        self.graph.expressions.append(self.next(), expression)

    def on_type(self, type: tree.types.Type, path: Path) -> None:
        self.graph.types.append(self.next(), type)

    def on_range(self, range: tree.types.Range, path: Path) -> None:
        self.graph.ranges.append(self.next(), range)


@dataclass(kw_only=True)
class SyntaxGraph:
    snippets: Bidirectional[tree.snippet.Snippet]
    signatures: Bidirectional[tree.snippet.Signature]
    slots: Bidirectional[tree.snippet.Slot]
    binds: Bidirectional[tree.snippet.Bind]
    labels: Bidirectional[tree.snippet.Label]
    instructions: Bidirectional[tree.snippet.Instruction]
    operands: Bidirectional[tree.snippet.Operand]
    immediates: Bidirectional[tree.snippet.Immediate]
    registers: Bidirectional[tree.snippet.Register]
    references: Bidirectional[tree.snippet.Reference]

    functions: Bidirectional[tree.function.Function]
    statements: Bidirectional[tree.function.Statement]
    literals: Bidirectional[tree.function.Literal]
    expressions: Bidirectional[tree.function.Expression]
    parameters: Bidirectional[tree.function.Parameter]

    types: Bidirectional[tree.types.Type]
    ranges: Bidirectional[tree.types.Range]

    @staticmethod
    def empty() -> SyntaxGraph:
        return SyntaxGraph(
            snippets=Bidirectional[tree.snippet.Snippet].empty(),
            signatures=Bidirectional[tree.snippet.Signature].empty(),
            slots=Bidirectional[tree.snippet.Slot].empty(),
            binds=Bidirectional[tree.snippet.Bind].empty(),
            labels=Bidirectional[tree.snippet.Label].empty(),
            instructions=Bidirectional[tree.snippet.Instruction].empty(),
            operands=Bidirectional[tree.snippet.Operand].empty(),
            immediates=Bidirectional[tree.snippet.Immediate].empty(),
            registers=Bidirectional[tree.snippet.Register].empty(),
            references=Bidirectional[tree.snippet.Reference].empty(),
            functions=Bidirectional[tree.function.Function].empty(),
            statements=Bidirectional[tree.function.Statement].empty(),
            literals=Bidirectional[tree.function.Literal].empty(),
            expressions=Bidirectional[tree.function.Expression].empty(),
            parameters=Bidirectional[tree.function.Parameter].empty(),
            types=Bidirectional[tree.types.Type].empty(),
            ranges=Bidirectional[tree.types.Range].empty(),
        )


def build_syntax_graph(
    generator: Generator,
    program: tree.Program,
) -> SyntaxGraph:
    visitor = NodesVisitor(generator)
    program.accept(visitor, Path())

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
