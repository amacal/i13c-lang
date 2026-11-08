from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class AddressId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("address", f"{self.value:<{length}}"))
