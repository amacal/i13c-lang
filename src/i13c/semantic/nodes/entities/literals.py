from typing import Dict

from i13c import ast
from i13c.core.mapping import OneToOne
from i13c.semantic.core import derive_width
from i13c.semantic.infra import Configuration
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.literals import Hex, Literal, LiteralId


def configure_literals() -> Configuration:
    return Configuration(
        builder=build_literals,
        produces=("entities/literals",),
        requires=frozenset({("graph", "syntax/graph")}),
    )


def build_literals(
    graph: SyntaxGraph,
) -> OneToOne[LiteralId, Literal]:
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

    return OneToOne[LiteralId, Literal].instance(literals)
