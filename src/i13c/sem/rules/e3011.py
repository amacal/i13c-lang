# from typing import List, Optional

# from i13c import ast, diag, err, sym


# def validate_called_symbol_arguments(
#     program: ast.Program,
#     symbols: sym.SymbolTable,
# ) -> List[diag.Diagnostic]:
#     diagnostics: List[diag.Diagnostic] = []

#     for function in program.functions:
#         if function.terminal:
#             if isinstance(function, ast.RegFunction):
#                 for statement in function.statements:
#                     if symbol := symbols.entries.get(statement.name):
#                         pass

#     return diagnostics


# def compare_arguments_with_parameters(
#     diagnosics: List[diag.Diagnostic],
#     arguments: List[sym.SigParameter],
#     parameters: List[ast.RegParameter],
# ) -> None:
#     if len(arguments) != len(parameters):
#         diagnosics.append(
#             err.report_e3011_called_argument_mismatch(
#                 parameters[0].ref if parameters else b"",
#                 len(arguments),
#                 len(parameters),
#             )
#         )
#         return

#     for index in range(len(arguments)):
#         argument = arguments[index]
#         parameter = parameters[index]

#         if argument.type.name != parameter.type.name:
#             diagnosics.append(
#                 err.report_e3011_called_argument_mismatch(
#                     parameter.ref,
#                     index,
#                     argument.type.name,
#                     parameter.type.name,
#                 )
#             )
