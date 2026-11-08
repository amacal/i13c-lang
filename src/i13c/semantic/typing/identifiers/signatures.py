from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class SignatureId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("signature", f"{self.value:<{length}}"))
