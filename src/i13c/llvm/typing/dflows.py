from dataclasses import dataclass


@dataclass(kw_only=True, repr=False)
class DataFlowSegment:
    # DFG Node -> DFG Nodes
    forward: dict[int, list[int]]
    backward: dict[int, list[int]]

    # Instruction -> DFG Values
    defs: list[list[int]]
    uses: list[list[int]]

    # Instruction -> DFG Values
    clobbers: list[list[int]]

    def add_instruction(self):
        self.defs.append([])
        self.uses.append([])
        self.clobbers.append([])

    def add_clobber(self, iid: int, ireg: int):
        self.clobbers[iid].append(ireg)

    def add_def(self, iid: int, ireg: int):
        self.defs[iid].append(ireg)

    def add_use(self, iid: int, ireg: int):
        self.uses[iid].append(ireg)

    def add_edge(self, src: int, dst: int):
        if src not in self.forward:
            self.forward[src] = [dst]
        else:
            self.forward[src].append(dst)

        if dst not in self.backward:
            self.backward[dst] = [src]
        else:
            self.backward[dst].append(src)


@dataclass(kw_only=True, repr=False)
class DataFlow:
    registers: list[bytes]
    segments: list[DataFlowSegment]
    seeds: list[tuple[int, int]]

    def add_segment(self) -> DataFlowSegment:
        segment = DataFlowSegment(
            forward={},
            backward={},
            defs=[],
            uses=[],
            clobbers=[],
        )

        self.segments.append(segment)
        return segment

    def add_register(self, reg: bytes) -> int:
        if reg in self.registers:
            ireg = self.registers.index(reg)
        else:
            self.registers.append(reg)
            ireg = len(self.registers) - 1

        return ireg

    def add_seed(self, src: int, dst: int):
        self.seeds.append((src, dst))
