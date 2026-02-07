from dataclasses import dataclass
from typing import List, Optional, Protocol, Union

from i13c import src


class Visitor(Protocol):
    def on_program(self, program: Program) -> None: ...
    def on_snippet(self, snippet: Snippet) -> None: ...
    def on_instruction(self, instruction: Instruction) -> None: ...
    def on_function(self, function: Function) -> None: ...
    def on_statement(self, statement: Statement) -> None: ...
    def on_literal(self, literal: Literal) -> None: ...
    def on_expression(self, expression: Expression) -> None: ...
    def on_operand(self, operand: Operand) -> None: ...
    def on_parameter(self, parameter: Parameter) -> None: ...


@dataclass(kw_only=True, eq=False)
class Type:
    name: bytes
    range: Optional[Range]


@dataclass(kw_only=True, eq=False)
class Range:
    lower: int
    upper: int


@dataclass(kw_only=True, eq=False)
class Register:
    ref: src.Span
    name: bytes


@dataclass(kw_only=True, eq=False)
class Immediate:
    ref: src.Span
    value: int


@dataclass(kw_only=True, eq=False)
class Reference:
    ref: src.Span
    name: bytes


Operand = Union[Register, Immediate, Reference]


@dataclass(kw_only=True, eq=False)
class IntegerLiteral:
    ref: src.Span
    value: int


@dataclass(kw_only=True, eq=False)
class Expression:
    ref: src.Span
    name: bytes


Literal = Union[IntegerLiteral]
Argument = Union[Literal, Expression]


@dataclass(kw_only=True, eq=False)
class Mnemonic:
    name: bytes


@dataclass(kw_only=True, eq=False)
class Instruction:
    ref: src.Span
    mnemonic: Mnemonic
    operands: List[Operand]

    def accept(self, visitor: Visitor) -> None:
        visitor.on_instruction(self)

        # avoid entering operands
        for operand in self.operands:
            visitor.on_operand(operand)


@dataclass(kw_only=True, eq=False)
class CallStatement:
    ref: src.Span
    name: bytes
    arguments: List[Argument]

    def accept(self, visitor: Visitor) -> None:
        visitor.on_statement(self)

        for argument in self.arguments:
            if isinstance(argument, IntegerLiteral):
                visitor.on_literal(argument)
            if isinstance(argument, Expression):
                visitor.on_expression(argument)


@dataclass(kw_only=True)
class ImmediateBinding:
    pass


Statement = Union[CallStatement]


@dataclass(kw_only=True)
class Binding:
    name: bytes


@dataclass(kw_only=True, eq=False)
class Slot:
    name: bytes
    type: Type
    bind: Binding


@dataclass(kw_only=True, eq=False)
class Parameter:
    ref: src.Span
    name: bytes
    type: Type

    def accept(self, visitor: Visitor) -> None:
        visitor.on_parameter(self)


@dataclass(kw_only=True, eq=False)
class Snippet:
    ref: src.Span
    name: bytes
    noreturn: bool
    slots: List[Slot]
    clobbers: List[Register]
    instructions: List[Instruction]

    def accept(self, visitor: Visitor) -> None:
        visitor.on_snippet(self)

        for instruction in self.instructions:
            instruction.accept(visitor)


@dataclass(kw_only=True, eq=False)
class Function:
    ref: src.Span
    name: bytes
    noreturn: bool
    parameters: List[Parameter]
    statements: List[CallStatement]

    def accept(self, visitor: Visitor) -> None:
        visitor.on_function(self)

        for parameter in self.parameters:
            parameter.accept(visitor)

        for statement in self.statements:
            statement.accept(visitor)


@dataclass(kw_only=True, eq=False)
class Program:
    functions: List[Function]
    snippets: List[Snippet]

    def accept(self, visitor: Visitor) -> None:
        visitor.on_program(self)

        for snippet in self.snippets:
            snippet.accept(visitor)

        for function in self.functions:
            function.accept(visitor)
