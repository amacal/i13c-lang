from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class MnemonicId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("mnemonic", f"{self.value:<{length}}"))
