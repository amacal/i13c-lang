from dataclasses import dataclass
from typing import Optional

from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.binds import BindId
from i13c.semantic.typing.entities.immediates import ImmediateId
from i13c.semantic.typing.entities.ranges import RangeId
from i13c.semantic.typing.entities.signatures import SignatureId
from i13c.semantic.typing.entities.slots import SlotId
from i13c.semantic.typing.entities.types import TypeId
from i13c.semantic.typing.resolutions.binds import BindResolution
from i13c.semantic.typing.resolutions.immediates import ImmediateResolution
from i13c.semantic.typing.resolutions.ranges import RangeResolution
from i13c.semantic.typing.resolutions.signatures import SignatureResolution
from i13c.semantic.typing.resolutions.slots import SlotResolution
from i13c.semantic.typing.resolutions.types import TypeResolution


@dataclass
class ResolutionNodes:
    binds: Optional[OneToOne[BindId, BindResolution]]
    immediates: Optional[OneToOne[ImmediateId, ImmediateResolution]]
    ranges: Optional[OneToOne[RangeId, RangeResolution]]
    signatures: Optional[OneToOne[SignatureId, SignatureResolution]]
    slots: Optional[OneToOne[SlotId, SlotResolution]]
    types: Optional[OneToOne[TypeId, TypeResolution]]
