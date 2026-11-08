
from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.expressions import Expression, ExpressionNode
from i13c.semantic.typing.identifiers.callsites import CallSiteId
from i13c.semantic.typing.identifiers.expressions import ExpressionId
from i13c.semantic.typing.identifiers.literals import LiteralId
from i13c.semantic.typing.identifiers.usages import UsageId
from i13c.syntax import tree


def configure_expressions() -> GraphNode:
    return GraphNode(
        builder=build_expressions,
        constraint=None,
        produces=("entities/expressions",),
        requires=frozenset({("graph", "syntax/graph")}),
    )


def build_expressions(
    graph: SyntaxGraph,
) -> OneToOne[ExpressionId, Expression]:
    expressions: dict[ExpressionId, Expression] = {}

    for nid, expression in graph.function.expressions.items():
        # derive expression ID from globally unique node ID
        expr_id = ExpressionId(value=nid.value)

        # prepare nodes and queue for traversal
        nodes: list[ExpressionNode] = []
        queue: list[tree.function.ExpressionTarget] = [expression.target]

        # perform a depth-first traversal of the expression tree
        while queue:
            this = queue.pop()

            if isinstance(this, tree.function.ExpressionNode):
                queue.append(this.target)

            # handle explicit literal nodes
            if isinstance(this, tree.function.Literal):
                nid = graph.function.literals.get_by_node(this)
                nodes.append(LiteralId(value=nid.value))

            # handle referenced usage nodes
            if isinstance(this, tree.function.Usage):
                nid = graph.function.usages.get_by_node(this)
                nodes.append(UsageId(value=nid.value))

            # handle triggered callsite nodes
            if isinstance(this, tree.function.CallSite):
                nid = graph.function.callsites.get_by_node(this)
                nodes.append(CallSiteId(value=nid.value))

        expressions[expr_id] = Expression(
            ref=expression.ref,
            nodes=nodes,
        )

    return OneToOne[ExpressionId, Expression].instance(expressions)
