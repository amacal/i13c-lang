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

    def append(
        self, id: NodeId, node: AstNode, /, ctx: Optional[AstCtx] = None
    ) -> None:
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
        self.graph.snippet.snippets.append(self.next(), snippet)

    def on_signature(self, signature: tree.Signature, path: Path) -> None:
        if isinstance(signature, tree.snippet.Signature):
            self.graph.snippet.signatures.append(
                self.next(), signature, ctx=path.find(tree.snippet.Snippet)
            )
        else:
            self.graph.function.signatures.append(
                self.next(), signature, ctx=path.find(tree.function.Function)
            )

    def on_slot(self, slot: tree.snippet.Slot, path: Path) -> None:
        self.graph.snippet.slots.append(self.next(), slot)

    def on_bind(self, bind: tree.snippet.Bind, path: Path) -> None:
        self.graph.snippet.binds.append(
            self.next(), bind, ctx=path.find(tree.snippet.Slot)
        )

    def on_label(self, label: tree.snippet.Label, path: Path) -> None:
        self.graph.snippet.labels.append(
            self.next(), label, ctx=path.find(tree.snippet.Snippet)
        )

    def on_instruction(self, instruction: tree.snippet.Instruction, path: Path) -> None:
        self.graph.snippet.instructions.append(self.next(), instruction)

    def on_mnemonic(self, mnemonic: tree.snippet.Mnemonic, path: Path) -> None:
        self.graph.snippet.mnemonics.append(self.next(), mnemonic)

    def on_operand(self, operand: tree.snippet.Operand, path: Path) -> None:
        self.graph.snippet.operands.append(self.next(), operand)

    def on_immediate(self, immediate: tree.snippet.Immediate, path: Path) -> None:
        self.graph.snippet.immediates.append(self.next(), immediate)

    def on_register(self, register: tree.snippet.Register, path: Path) -> None:
        self.graph.snippet.registers.append(self.next(), register)

    def on_reference(self, reference: tree.snippet.Reference, path: Path) -> None:
        self.graph.snippet.references.append(
            self.next(), reference, ctx=path.find(tree.snippet.Snippet)
        )

    def on_address(self, address: tree.snippet.Address, path: Path) -> None:
        self.graph.snippet.addresses.append(self.next(), address)

    def on_function(self, function: tree.function.Function, path: Path) -> None:
        self.graph.function.functions.append(self.next(), function)

    def on_parameter(self, parameter: tree.function.Parameter, path: Path) -> None:
        self.graph.function.parameters.append(self.next(), parameter)

    def on_statement(self, statement: tree.function.Statement, path: Path) -> None:
        self.graph.function.statements.append(self.next(), statement)

    def on_literal(self, literal: tree.function.Literal, path: Path) -> None:
        self.graph.function.literals.append(self.next(), literal)

    def on_expression(self, expression: tree.function.Expression, path: Path) -> None:
        self.graph.function.expressions.append(self.next(), expression)

    def on_type(self, type: tree.types.Type, path: Path) -> None:
        self.graph.types.append(self.next(), type)

    def on_range(self, range: tree.types.Range, path: Path) -> None:
        self.graph.ranges.append(self.next(), range)


@dataclass(kw_only=True)
class Snippet:
    snippets: Bidirectional[tree.snippet.Snippet, None]
    signatures: Bidirectional[tree.snippet.Signature, tree.snippet.Snippet]
    slots: Bidirectional[tree.snippet.Slot, None]
    binds: Bidirectional[tree.snippet.Bind, tree.snippet.Slot]
    labels: Bidirectional[tree.snippet.Label, tree.snippet.Snippet]
    instructions: Bidirectional[tree.snippet.Instruction, None]
    mnemonics: Bidirectional[tree.snippet.Mnemonic, None]
    operands: Bidirectional[tree.snippet.Operand, None]
    immediates: Bidirectional[tree.snippet.Immediate, None]
    registers: Bidirectional[tree.snippet.Register, None]
    references: Bidirectional[tree.snippet.Reference, tree.snippet.Snippet]
    addresses: Bidirectional[tree.snippet.Address, None]


@dataclass(kw_only=True)
class Function:
    functions: Bidirectional[tree.function.Function, None]
    signatures: Bidirectional[tree.function.Signature, tree.function.Function]
    statements: Bidirectional[tree.function.Statement, None]
    literals: Bidirectional[tree.function.Literal, None]
    expressions: Bidirectional[tree.function.Expression, None]
    parameters: Bidirectional[tree.function.Parameter, None]


@dataclass(kw_only=True)
class SyntaxGraph:
    snippet: Snippet
    function: Function

    types: Bidirectional[tree.types.Type, None]
    ranges: Bidirectional[tree.types.Range, None]

    @staticmethod
    def empty() -> SyntaxGraph:
        return SyntaxGraph(
            snippet=Snippet(
                snippets=Bidirectional[tree.snippet.Snippet, None].empty(),
                signatures=Bidirectional[
                    tree.snippet.Signature, tree.snippet.Snippet
                ].empty(),
                slots=Bidirectional[tree.snippet.Slot, None].empty(),
                binds=Bidirectional[tree.snippet.Bind, tree.snippet.Slot].empty(),
                labels=Bidirectional[tree.snippet.Label, tree.snippet.Snippet].empty(),
                instructions=Bidirectional[tree.snippet.Instruction, None].empty(),
                mnemonics=Bidirectional[tree.snippet.Mnemonic, None].empty(),
                operands=Bidirectional[tree.snippet.Operand, None].empty(),
                immediates=Bidirectional[tree.snippet.Immediate, None].empty(),
                registers=Bidirectional[tree.snippet.Register, None].empty(),
                references=Bidirectional[
                    tree.snippet.Reference, tree.snippet.Snippet
                ].empty(),
                addresses=Bidirectional[tree.snippet.Address, None].empty(),
            ),
            function=Function(
                functions=Bidirectional[tree.function.Function, None].empty(),
                signatures=Bidirectional[
                    tree.function.Signature, tree.function.Function
                ].empty(),
                statements=Bidirectional[tree.function.Statement, None].empty(),
                literals=Bidirectional[tree.function.Literal, None].empty(),
                expressions=Bidirectional[tree.function.Expression, None].empty(),
                parameters=Bidirectional[tree.function.Parameter, None].empty(),
            ),
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
