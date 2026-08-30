from dataclasses import dataclass

from i13c.semantic.typing.resolutions.signatures import SignatureAcceptance


@dataclass(kw_only=True)
class Entrypoint:
    target: SignatureAcceptance
