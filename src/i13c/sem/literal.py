from dataclasses import dataclass
from typing import Dict
from typing import Literal as Kind
from typing import Optional

from i13c import ast
from i13c.src import Span
from i13c.sem.core import Width, derive_width
from i13c.sem.syntax import SyntaxGraph

LiteralKind = Kind[b"hex"]


@dataclass(kw_only=True)
class Hex:
    value: int
    width: Optional[Width]


@dataclass(kw_only=True, frozen=True)
class LiteralId:
    value: int


@dataclass(kw_only=True)
class Literal:
    ref: Span
    kind: LiteralKind
    target: Hex


def build_literals(
    graph: SyntaxGraph,
) -> Dict[LiteralId, Literal]:
    literals: Dict[LiteralId, Literal] = {}

    for nid, literal in graph.nodes.literals.items():
        assert isinstance(literal, ast.IntegerLiteral)

        # derive literal ID from globally unique node ID
        id = LiteralId(value=nid.value)

        literals[id] = Literal(
            ref=literal.ref,
            kind=b"hex",
            target=Hex(
                value=literal.value,
                width=derive_width(literal.value),
            ),
        )

    return literals
