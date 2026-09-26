from dataclasses import dataclass


@dataclass(kw_only=True, repr=False)
class LivenessSegment:
    # Instruction -> DFG Values
    live_in: list[set[int]]
    live_out: list[set[int]]

    # Instruction -> DFG Nodes
    # directly inherited from the DFG
    clobbers: list[list[int]]

    def instructions(self) -> int:
        return len(self.clobbers)


@dataclass(kw_only=True, repr=False)
class Liveness:
    registers: list[bytes]
    segments: list[LivenessSegment]
    seeds: list[tuple[int, int]]
