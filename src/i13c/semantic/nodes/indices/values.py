from typing import Dict, List

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToMany, OneToOne
from i13c.semantic.typing.entities.statements import StatementId
from i13c.semantic.typing.entities.values import ValueId
from i13c.semantic.typing.resolutions.values import ValueAcceptance


def configure_values_by_statements() -> GraphNode:
    return GraphNode(
        builder=build_values_by_statements,
        constraint=None,
        produces=("indices/values/statements",),
        requires=frozenset(
            {
                ("values", "resolutions/values/accepted"),
            }
        ),
    )


def build_values_by_statements(
    values: OneToOne[ValueId, ValueAcceptance],
) -> OneToMany[StatementId, ValueAcceptance]:
    index: Dict[StatementId, List[ValueAcceptance]] = {}

    for _, entry in values.items():
        stmt_id = entry.get_statement(StatementId.from_context)
        data = index.get(stmt_id)

        if data is None:
            index[stmt_id] = [entry]
        else:
            data.append(entry)

    return OneToMany[StatementId, ValueAcceptance].instance(index)
