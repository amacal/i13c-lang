from dataclasses import dataclass
from typing import List, Optional, Protocol, Union

import i13c.syntax.tree.literals as literals
import i13c.syntax.tree.types as types
from i13c.syntax.source import Span
from i13c.syntax.tree.core import Path


class Visitor(Protocol):
    def on_function(self, function: Function, path: Path) -> None: ...
    def on_flags(self, flags: Flags, path: Path) -> None: ...
    def on_signature(self, signature: Signature, path: Path) -> None: ...
    def on_statement(self, statement: Statement, path: Path) -> None: ...
    def on_callsite(self, callsite: CallStatement, path: Path) -> None: ...
    def on_assign(self, assign: AssignStatement, path: Path) -> None: ...
    def on_value(self, value: Value, path: Path) -> None: ...
    def on_literal(self, literal: Literal, path: Path) -> None: ...
    def on_expression(self, expression: Expression, path: Path) -> None: ...
    def on_parameter(self, parameter: Parameter, path: Path) -> None: ...

    # types related
    def on_type(self, type: types.Type, path: Path) -> None: ...
    def on_range(self, range: types.Range, path: Path) -> None: ...


@dataclass(kw_only=True, eq=False)
class Literal:
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
        visitor.on_callsite(self, path)

        with path.push(self) as node:
            for argument in self.arguments:
                if isinstance(argument, Literal):
                    visitor.on_literal(argument, node)

                if isinstance(argument, Expression):
                    visitor.on_expression(argument, node)


ValueExpression = Union[Literal, Expression]


@dataclass(kw_only=True, eq=False)
class Value:
    ref: Span
    name: bytes
    type: types.Type

    def accept(self, visitor: Visitor, path: Path) -> None:
        visitor.on_value(self, path)

        with path.push(self) as node:
            self.type.accept(visitor, node)


@dataclass(kw_only=True, eq=False)
class AssignStatement:
    ref: Span
    destination: Value
    expression: ValueExpression

    def accept(self, visitor: Visitor, path: Path) -> None:
        visitor.on_assign(self, path)

        with path.push(self) as node:
            # first visit the destination
            self.destination.accept(visitor, node)

            # then the expression
            self.expression.accept(visitor, node)


@dataclass(kw_only=True, eq=False)
class Signature:
    ref: Span
    name: bytes
    params: List[Parameter]

    def accept(self, visitor: Visitor, path: Path) -> None:
        visitor.on_signature(self, path)

        with path.push(self) as node:
            for entry in self.params:
                entry.accept(visitor, node)


StatementTarget = Union[CallStatement, AssignStatement]

@dataclass(kw_only=True, eq=False)
class Statement:
    ref: Span
    target: StatementTarget

    def accept(self, visitor: Visitor, path: Path) -> None:
        visitor.on_statement(self, path)

        with path.push(self) as node:
            self.target.accept(visitor, node)


@dataclass(kw_only=True, eq=False)
class Flags:
    ref: Span
    noreturn: Optional[bool]

    def accept(self, visitor: Visitor, path: Path) -> None:
        visitor.on_flags(self, path)


@dataclass(kw_only=True, eq=False)
class Function:
    ref: Span
    signature: Signature
    flags: Optional[Flags]
    statements: List[Statement]

    def accept(self, visitor: Visitor, path: Path) -> None:
        visitor.on_function(self, path)

        with path.push(self) as node:
            self.signature.accept(visitor, node)

            if self.flags is not None:
                self.flags.accept(visitor, node)

            for statement in self.statements:
                statement.accept(visitor, node)
