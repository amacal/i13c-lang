from dataclasses import dataclass
from typing import List

from i13c.semantic.typing.resolutions.signatures import SignatureAcceptance


@dataclass(kw_only=True)
class CallGraph:
    target: SignatureAcceptance
    forward: List[SignatureAcceptance]
    backward: List[SignatureAcceptance]
