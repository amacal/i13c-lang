from dataclasses import dataclass
from typing import Optional, Union

from i13c.llvm.typing.instructions.core import ComputedAddress, RelativeAddress


@dataclass(kw_only=True)
class LabelArtifact:
    target: int
    offset: int


@dataclass(kw_only=True)
class RelocationArtifact:
    target: int
    offset: int


class UnreachableEncodingError(Exception):
    pass


class Address:
    @staticmethod
    def index_uses_rsp(addr: Union[ComputedAddress, RelativeAddress]) -> bool:
        return (
            addr.scaler.index_uses_rsp() if isinstance(addr, ComputedAddress) else False
        )

    @staticmethod
    def scale_offset(addr: Union[ComputedAddress, RelativeAddress]) -> int:
        return addr.scaler.scale_offset() if isinstance(addr, ComputedAddress) else 0

    @staticmethod
    def index_or_none(addr: Union[ComputedAddress, RelativeAddress]) -> Optional[int]:
        return (
            addr.scaler.index_or_none() if isinstance(addr, ComputedAddress) else None
        )

    @staticmethod
    def base_or_none(addr: Union[ComputedAddress, RelativeAddress]) -> Optional[int]:
        return addr.base.value_or_none() if isinstance(addr, ComputedAddress) else None

    @staticmethod
    def base_is_available(addr: Union[ComputedAddress, RelativeAddress]) -> bool:
        return addr.base.is_available() if isinstance(addr, ComputedAddress) else False

    @staticmethod
    def base_uses_rbp_r13(addr: Union[ComputedAddress, RelativeAddress]) -> bool:
        return addr.base.low3bits() == 5 if isinstance(addr, ComputedAddress) else False

    @staticmethod
    def is_relative(addr: Union[ComputedAddress, RelativeAddress]) -> bool:
        return isinstance(addr, RelativeAddress)
