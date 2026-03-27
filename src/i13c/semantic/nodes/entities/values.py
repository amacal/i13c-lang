from typing import Dict, Optional

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.core import Identifier, Range, Type, default_range, width_from_range
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.expressions import ExpressionId
from i13c.semantic.typing.entities.literals import LiteralId
from i13c.semantic.typing.entities.values import Expression, Value, ValueId
from i13c.syntax import tree


def configure_values() -> GraphNode:
    return GraphNode(
        builder=build_values,
        constraint=None,
        produces=("entities/values",),
        requires=frozenset({("graph", "syntax/graph")}),
    )


def build_values(
    graph: SyntaxGraph,
) -> OneToOne[ValueId, Value]:
    values: Dict[ValueId, Value] = {}

    for nid, statement in graph.statements.items():
        expression: Optional[Expression] = None

        # accept only value statements
        if not isinstance(statement, tree.ValueStatement):
            continue

        match statement.expr:
            case tree.IntegerLiteral() as lit:
                # find literal by AST node
                lid = graph.literals.get_by_node(lit)

                expression = Expression(
                    kind=b"literal",
                    target=LiteralId(value=lid.value),
                )
            case tree.Expression() as expr:
                # find expression by AST node
                eid = graph.expressions.get_by_node(expr)

                expression = Expression(
                    kind=b"expression",
                    target=ExpressionId(value=eid.value),
                )

        # derive value ID from globally unique node ID
        value_id = ValueId(value=nid.value)
        assert expression is not None

        # default width and ranges for declared type
        range: Range = default_range(statement.type.name)
        ident = Identifier(name=statement.name)

        # override ranges if specified
        if statement.type.range is not None:
            range = Range(
                lower=statement.type.range.lower,
                upper=statement.type.range.upper,
            )

        # derive width from ranges
        width = width_from_range(range)

        # construct slot type with range or default width
        type = Type(
            name=statement.type.name,
            width=width,
            range=range,
        )

        values[value_id] = Value(
            id=value_id,
            ref=statement.ref,
            expr=expression,
            ident=ident,
            type=type,
        )

    return OneToOne[ValueId, Value].instance(values)
