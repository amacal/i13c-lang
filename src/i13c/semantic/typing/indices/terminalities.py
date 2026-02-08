from dataclasses import dataclass


@dataclass(kw_only=True)
class Terminality:
    noreturn: bool

    def describe(self) -> str:
        return f"noreturn={self.noreturn}"
