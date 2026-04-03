from dataclasses import dataclass

from i13c.llvm.typing.flows import BlockId


@dataclass(kw_only=True)
class Call:
    target: BlockId

    def native(self) -> str:
        return f"call {self.target.identify(1)}"

@dataclass(kw_only=True)
class Label:
    id: BlockId

    def native(self) -> str:
        return f"label {self.id.identify(1)}"


@dataclass(kw_only=True)
class Return:
    def native(self) -> str:
        return "ret"


@dataclass(kw_only=True)
class SysCall:
    def native(self) -> str:
        return "syscall"


@dataclass(kw_only=True)
class Jump:
    target: BlockId

    def native(self) -> str:
        return f"jmp {self.target.identify(1)}"


@dataclass(kw_only=True)
class Nop:
    def native(self) -> str:
        return "nop"
