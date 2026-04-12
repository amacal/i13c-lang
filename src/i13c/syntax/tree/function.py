from dataclasses import dataclass
from typing import List, Protocol, Union

import i13c.syntax.tree.literals as literals
import i13c.syntax.tree.types as types
from i13c.syntax.source import Span
from i13c.syntax.tree.core import Path


class Visitor(Protocol):
    def on_function(self, function: Function, path: Path) -> None: ...
    def on_statement(self, statement: Statement, path: Path) -> None: ...
    def on_literal(self, literal: Literal, path: Path) -> None: ...
    def on_expression(self, expression: Expression, path: Path) -> None: ...
    def on_parameter(self, parameter: Parameter, path: Path) -> None: ...

    # types related
    def on_type(self, type: types.Type, path: Path) -> None: ...
    def on_range(self, range: types.Range, path: Path) -> None: ...


@dataclass(kw_only=True, eq=False)
class IntegerLiteral:
    ref: Span
    value: literals.Hex

    def accept(self, visitor: Visitor, path: Path) -> None:
        visitor.on_literal(self, path)


@dataclass(kw_only=True, eq=False)
class Expression:
    ref: Span
    name: bytes

    def accept(self, visitor: Visitor, path: Path) -> None:
        visitor.on_expression(self, path)


Literal = Union[IntegerLiteral]
Argument = Union[Literal, Expression]


@dataclass(kw_only=True, eq=False)
class Parameter:
    ref: Span
    name: bytes
    type: types.Type

    def accept(self, visitor: Visitor, path: Path) -> None:
        visitor.on_parameter(self, path)

        with path.push(self) as node:
            self.type.accept(visitor, node)


@dataclass(kw_only=True, eq=False)
class CallStatement:
    ref: Span
    name: bytes
    arguments: List[Argument]

    def accept(self, visitor: Visitor, path: Path) -> None:
        visitor.on_statement(self, path)

        with path.push(self) as node:
            for argument in self.arguments:
                if isinstance(argument, IntegerLiteral):
                    visitor.on_literal(argument, node)

                if isinstance(argument, Expression):
                    visitor.on_expression(argument, node)


ValueExpression = Union[Literal, Expression]


@dataclass(kw_only=True, eq=False)
class ValueStatement:
    ref: Span
    name: bytes
    type: types.Type
    expr: ValueExpression

    def accept(self, visitor: Visitor, path: Path) -> None:
        visitor.on_statement(self, path)

        with path.push(self) as node:
            # first visit the type
            self.type.accept(visitor, node)

            # then the expression
            self.expr.accept(visitor, node)


Statement = Union[CallStatement, ValueStatement]


@dataclass(kw_only=True, eq=False)
class Function:
    ref: Span
    name: bytes
    noreturn: bool
    parameters: List[Parameter]
    statements: List[Statement]

    def accept(self, visitor: Visitor, path: Path) -> None:
        visitor.on_function(self, path)

        with path.push(self) as node:
            for parameter in self.parameters:
                parameter.accept(visitor, node)

            for statement in self.statements:
                statement.accept(visitor, node)
