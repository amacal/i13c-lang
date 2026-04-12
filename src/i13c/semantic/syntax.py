from dataclasses import dataclass
from typing import Dict, Iterable, Optional, Tuple, TypeVar

from i13c.core.generator import Generator
from i13c.core.graph import GraphGroup, GraphNode
from i13c.syntax import tree
from i13c.syntax.tree.core import Path

AstNode = TypeVar("AstNode")
AstCtx = TypeVar("AstCtx")


@dataclass(kw_only=True, frozen=True)
class NodeId:
    value: int


@dataclass(kw_only=True)
class Bidirectional[AstNode, AstCtx]:
    node_to_id: Dict[AstNode, NodeId]
    id_to_node: Dict[NodeId, AstNode]
    id_to_ctx: Dict[NodeId, AstCtx]

    @staticmethod
    def empty() -> Bidirectional[AstNode, AstCtx]:
        return Bidirectional(node_to_id={}, id_to_node={}, id_to_ctx={})

    def append(self, id: NodeId, node: AstNode, /, ctx: Optional[AstCtx] = None) -> None:
        self.node_to_id[node] = id
        self.id_to_node[id] = node

        if ctx is not None:
            self.id_to_ctx[id] = ctx

    def items(self) -> Iterable[Tuple[NodeId, AstNode]]:
        return self.id_to_node.items()

    def get_ctx(self, node_id: NodeId) -> AstCtx:
        return self.id_to_ctx[node_id]

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
        self.graph.references.append(self.next(), reference, ctx=path.find(tree.snippet.Snippet))

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
    snippets: Bidirectional[tree.snippet.Snippet, None]
    signatures: Bidirectional[tree.snippet.Signature, None]
    slots: Bidirectional[tree.snippet.Slot, None]
    binds: Bidirectional[tree.snippet.Bind, None]
    labels: Bidirectional[tree.snippet.Label, None]
    instructions: Bidirectional[tree.snippet.Instruction, None]
    operands: Bidirectional[tree.snippet.Operand, None]
    immediates: Bidirectional[tree.snippet.Immediate, None]
    registers: Bidirectional[tree.snippet.Register, None]
    references: Bidirectional[tree.snippet.Reference, tree.snippet.Snippet]

    functions: Bidirectional[tree.function.Function, None]
    statements: Bidirectional[tree.function.Statement, None]
    literals: Bidirectional[tree.function.Literal, None]
    expressions: Bidirectional[tree.function.Expression, None]
    parameters: Bidirectional[tree.function.Parameter, None]

    types: Bidirectional[tree.types.Type, None]
    ranges: Bidirectional[tree.types.Range, None]

    @staticmethod
    def empty() -> SyntaxGraph:
        return SyntaxGraph(
            snippets=Bidirectional[tree.snippet.Snippet, None].empty(),
            signatures=Bidirectional[tree.snippet.Signature, None].empty(),
            slots=Bidirectional[tree.snippet.Slot, None].empty(),
            binds=Bidirectional[tree.snippet.Bind, None].empty(),
            labels=Bidirectional[tree.snippet.Label, None].empty(),
            instructions=Bidirectional[tree.snippet.Instruction, None].empty(),
            operands=Bidirectional[tree.snippet.Operand, None].empty(),
            immediates=Bidirectional[tree.snippet.Immediate, None].empty(),
            registers=Bidirectional[tree.snippet.Register, None].empty(),
            references=Bidirectional[tree.snippet.Reference, tree.snippet.Snippet].empty(),
            functions=Bidirectional[tree.function.Function, None].empty(),
            statements=Bidirectional[tree.function.Statement, None].empty(),
            literals=Bidirectional[tree.function.Literal, None].empty(),
            expressions=Bidirectional[tree.function.Expression, None].empty(),
            parameters=Bidirectional[tree.function.Parameter, None].empty(),
            types=Bidirectional[tree.types.Type, None].empty(),
            ranges=Bidirectional[tree.types.Range, None].empty(),
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
