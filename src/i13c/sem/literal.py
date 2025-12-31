from dataclasses import dataclass
from typing import Dict
from typing import Literal as Kind

from i13c import ast
from i13c.sem.core import Width, derive_width
from i13c.sem.syntax import SyntaxGraph
from i13c.src import Span

LiteralKind = Kind[b"hex"]


@dataclass(kw_only=True)
class Hex:
    value: int
    width: Width

    def describe(self) -> str:
        bytes_ = self.width // 8
        hex_digits = max(2, bytes_ * 2)

        return f"value=0x{self.value:0{hex_digits}x}"


@dataclass(kw_only=True, frozen=True)
class LiteralId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("literal", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Literal:
    ref: Span
    kind: LiteralKind
    target: Hex

    def describe(self) -> str:
        return f"kind={self.kind.decode()} {self.target.describe()}"


def build_literals(
    graph: SyntaxGraph,
) -> Dict[LiteralId, Literal]:
    literals: Dict[LiteralId, Literal] = {}

    for nid, literal in graph.literals.items():
        assert isinstance(literal, ast.IntegerLiteral)

        # derive literal ID from globally unique node ID
        literal_id = LiteralId(value=nid.value)

        literals[literal_id] = Literal(
            ref=literal.ref,
            kind=b"hex",
            target=Hex(
                value=literal.value,
                width=derive_width(literal.value),
            ),
        )

    return literals
