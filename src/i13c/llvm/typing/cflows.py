from dataclasses import dataclass


@dataclass(kw_only=True, repr=False)
class ControlFlowSegment:
    # CFG Nodes
    forward: list[int]
    backward: list[int]

    @staticmethod
    def empty() -> ControlFlowSegment:
        return ControlFlowSegment(forward=[], backward=[])


@dataclass(kw_only=True, repr=False)
class ControlFlow:
    gates: list[int]
    segments: list[ControlFlowSegment]

    @staticmethod
    def create(segments: int) -> ControlFlow:
        return ControlFlow(
            gates=[0],
            segments=[ControlFlowSegment.empty() for _ in range(segments)],
        )

    def add_edge(self, src: int, dst: int):
        self.segments[src].forward.append(dst)
        self.segments[dst].backward.append(src)

    def set_exit(self, idx: int):
        self.gates.append(idx)
