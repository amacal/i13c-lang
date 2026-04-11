# ruff: noqa: F401
# pyright: reportUnusedImport=false

from dataclasses import dataclass
from typing import List, Protocol

import i13c.syntax.tree.function as function
import i13c.syntax.tree.literals as literals
import i13c.syntax.tree.snippet as snippet
import i13c.syntax.tree.types as types


class Visitor(Protocol):
    def on_program(self, program: Program) -> None: ...

    # snippet related
    def on_snippet(self, snippet: snippet.Snippet) -> None: ...
    def on_slot(self, slot: snippet.Slot) -> None: ...
    def on_bind(self, bind: snippet.Bind) -> None: ...
    def on_instruction(self, instruction: snippet.Instruction) -> None: ...

    # function related
    def on_function(self, function: function.Function) -> None: ...
    def on_statement(self, statement: function.Statement) -> None: ...
    def on_literal(self, literal: function.Literal) -> None: ...
    def on_expression(self, expression: function.Expression) -> None: ...
    def on_operand(self, operand: snippet.Operand) -> None: ...
    def on_parameter(self, parameter: function.Parameter) -> None: ...

    # types related
    def on_type(self, type: types.Type) -> None: ...
    def on_range(self, range: types.Range) -> None: ...



@dataclass(kw_only=True, eq=False)
class Program:
    functions: List[function.Function]
    snippets: List[snippet.Snippet]

    def accept(self, visitor: Visitor) -> None:
        visitor.on_program(self)

        for entry in self.snippets:
            entry.accept(visitor)

        for entry in self.functions:
            entry.accept(visitor)
