from dataclasses import asdict, dataclass
from typing import Any, Dict, Iterable, Optional, Protocol, Tuple, TypeVar, Union

from i13c import ast

AstNode = TypeVar("AstNode")


@dataclass(kw_only=True, frozen=True)
class NodeId:
    value: int


class BidirectionalLike(Protocol):
    def as_dict(self) -> Dict[int, Dict[str, Any]]: ...


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

    def as_dict(self) -> Dict[int, Dict[str, Any]]:
        return {
            k.value: asdict(v)  # type: ignore[reportUnknownMemberType]
            for k, v in self.id_to_node.items()
        }


class NodesVisitor:
    def __init__(self) -> None:
        self.counter = 0
        self.graph = SyntaxGraph.empty()

    def next(self) -> NodeId:
        self.counter += 1
        nid = NodeId(value=self.counter)

        return nid

    def on_program(self, program: ast.Program) -> None:
        pass

    def on_snippet(self, snippet: ast.Snippet) -> None:
        self.graph.snippets.append(self.next(), snippet)

    def on_instruction(self, instruction: ast.Instruction) -> None:
        self.graph.instructions.append(self.next(), instruction)

    def on_function(self, function: ast.Function) -> None:
        self.graph.functions.append(self.next(), function)

    def on_statement(self, statement: ast.Statement) -> None:
        self.graph.statements.append(self.next(), statement)

    def on_literal(self, literal: ast.Literal) -> None:
        self.graph.literals.append(self.next(), literal)

    def on_operand(self, operand: ast.Operand) -> None:
        self.graph.operands.append(self.next(), operand)


@dataclass(kw_only=True)
class SyntaxGraph:
    snippets: Bidirectional[ast.Snippet]
    operands: Bidirectional[ast.Operand]
    instructions: Bidirectional[ast.Instruction]
    functions: Bidirectional[ast.Function]
    statements: Bidirectional[ast.Statement]
    literals: Bidirectional[ast.Literal]

    @staticmethod
    def empty() -> "SyntaxGraph":
        return SyntaxGraph(
            snippets=Bidirectional[ast.Snippet].empty(),
            operands=Bidirectional[ast.Operand].empty(),
            instructions=Bidirectional[ast.Instruction].empty(),
            functions=Bidirectional[ast.Function].empty(),
            statements=Bidirectional[ast.Statement].empty(),
            literals=Bidirectional[ast.Literal].empty(),
        )

    def as_dict(
        self, key: str
    ) -> Optional[Union[Dict[int, Dict[str, Any]], Dict[str, Any]]]:
        # split the key and id if present
        key, id = key.split("#", maxsplit=1) if "#" in key else (key, None)

        # get the appropriate relation
        field: Optional[BidirectionalLike] = getattr(self, key, None)

        # guard the missing field case
        data = field.as_dict() if field else {}

        # return either the full data or the specific node
        return data if not id else data.get(int(id))


def build_syntax_graph(program: ast.Program) -> SyntaxGraph:
    visitor = NodesVisitor()
    program.accept(visitor)

    return visitor.graph
