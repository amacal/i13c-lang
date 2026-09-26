from dataclasses import dataclass


@dataclass(kw_only=True, repr=False)
class AllocationSegment:
    colors: dict[int, int]
    spills: dict[int, int]


@dataclass(kw_only=True, repr=False)
class Allocation:
    # vregs to index mapping
    registers: list[bytes]

    # pregs to index mapping
    palette: list[bytes]

    # pregs clobbered by function calls
    clobbers: list[bytes]

    # all segments
    segments: list[AllocationSegment]

    # initial vreg -> preg
    seeds: list[tuple[int, int]]

    def get_slots(self) -> int:
        slot = 0

        for segment in self.segments:
            for entry in segment.spills.values():
                slot = max(slot, entry + 1)

        return slot

    def get_used(self) -> set[bytes]:
        used: set[bytes] = set()

        for segment in self.segments:
            for idx in segment.colors.values():
                used.add(self.palette[idx])

        for clobber in self.clobbers:
            used.add(clobber)

        return used
