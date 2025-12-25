from typing import List

from i13c.sem.nodes import Call, Function


def resolve_call_candidates_by_arity(functions: List[Function]) -> None:
    for fn in functions:
        for stmt in fn.body:
            if not isinstance(stmt, Call):
                continue

            # keep only functions with matching arity
            stmt.candidates = [
                fn
                for fn in stmt.candidates
                if len(fn.parameters) == len(stmt.arguments)
            ]


def resolve_call_candidates_by_type(functions: List[Function]) -> None:

    def fits(stmt: Call, fn: Function) -> bool:
        for arg, param in zip(stmt.arguments, fn.parameters):
            val = arg.value.value
            typ = param.type.name

            if typ == b"u8" and not (0 <= val <= 0xFF):
                return False
            if typ == b"u16" and not (0 <= val <= 0xFFFF):
                return False
            if typ == b"u32" and not (0 <= val <= 0xFFFFFFFF):
                return False
            if typ == b"u64" and not (0 <= val <= 0xFFFFFFFFFFFFFFFF):
                return False

        return True

    for fn in functions:
        for stmt in fn.body:
            if not isinstance(stmt, Call):
                continue

            # keep only functions with matching argument types
            stmt.candidates = [fn for fn in stmt.candidates if fits(stmt, fn)]
