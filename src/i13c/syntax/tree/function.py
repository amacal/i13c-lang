from dataclasses import dataclass
from typing import List, Protocol, Union

from i13c.syntax.source import Span
from i13c.syntax.tree import types


class Visitor(Protocol):
    def on_function(self, function: Function) -> None: ...
    def on_statement(self, statement: Statement) -> None: ...
    def on_literal(self, literal: Literal) -> None: ...
    def on_expression(self, expression: Expression) -> None: ...
    def on_parameter(self, parameter: Parameter) -> None: ...


@dataclass(kw_only=True, eq=False)
class IntegerLiteral:
    ref: Span
    value: bytes


@dataclass(kw_only=True, eq=False)
class Expression:
    ref: Span
    name: bytes


Literal = Union[IntegerLiteral]
Argument = Union[Literal, Expression]


@dataclass(kw_only=True, eq=False)
class Parameter:
    ref: Span
    name: bytes
    type: types.Type

    def accept(self, visitor: Visitor) -> None:
        visitor.on_parameter(self)


@dataclass(kw_only=True, eq=False)
class CallStatement:
    ref: Span
    name: bytes
    arguments: List[Argument]

    def accept(self, visitor: Visitor) -> None:
        visitor.on_statement(self)

        for argument in self.arguments:
            if isinstance(argument, IntegerLiteral):
                visitor.on_literal(argument)

            if isinstance(argument, Expression):
                visitor.on_expression(argument)


ValueExpression = Union[Literal, Expression]


@dataclass(kw_only=True, eq=False)
class ValueStatement:
    ref: Span
    name: bytes
    type: types.Type
    expr: ValueExpression

    def accept(self, visitor: Visitor) -> None:
        visitor.on_statement(self)

        if isinstance(self.expr, IntegerLiteral):
            visitor.on_literal(self.expr)

        if isinstance(self.expr, Expression):
            visitor.on_expression(self.expr)


Statement = Union[CallStatement, ValueStatement]


@dataclass(kw_only=True, eq=False)
class Function:
    ref: Span
    name: bytes
    noreturn: bool
    parameters: List[Parameter]
    statements: List[Statement]

    def accept(self, visitor: Visitor) -> None:
        visitor.on_function(self)

        for parameter in self.parameters:
            parameter.accept(visitor)

        for statement in self.statements:
            statement.accept(visitor)
