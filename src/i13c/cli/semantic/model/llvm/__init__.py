from typing import Any, Dict

from i13c.cli.semantic.model.abstract import AbstractListExtractor
from i13c.cli.semantic.model.llvm.blocks import (
    BlockInstructionsListExtractor,
    BlockListExtractor,
)
from i13c.cli.semantic.model.llvm.functions import (
    BlocksListExtractor,
    EntriesListExtractor,
    ExitsListExtractor,
    InstructionsInFunctionsListExtractor,
    IntervalPressureInFunctionsListExtractor,
    IntervalsInFunctionsListExtractor,
    StackFrameInFunctionsListExtractor,
)
from i13c.cli.semantic.model.llvm.instructions import InstructionsListExtractor
from i13c.cli.semantic.model.llvm.patches import (
    PatchesOfBindingsListExtractor,
    PatchesOfCallsitesListExtractor,
    PatchesOfClobbersListExtractor,
    PatchesOfSnapshotsListExtractor,
    PatchesOfStackFramesListExtractor,
)
from i13c.cli.semantic.model.llvm.registers import (
    BlockRegistersListExtractor,
    InstructionRegistersListExtractor,
)

LLVM: Dict[str, AbstractListExtractor[Any]] = {
    "llvm/blocks": BlockListExtractor,
    "llvm/instructions": BlockInstructionsListExtractor,
    "llvm/functions/entries": EntriesListExtractor,
    "llvm/functions/exits": ExitsListExtractor,
    "llvm/functions/blocks": BlocksListExtractor,
    "llvm/functions/intervals": IntervalsInFunctionsListExtractor,
    "llvm/functions/intervals/pressure": IntervalPressureInFunctionsListExtractor,
    "llvm/functions/stackframes": StackFrameInFunctionsListExtractor,
    "llvm/functions/instructions": InstructionsInFunctionsListExtractor,
    "llvm/registers/instructions": InstructionRegistersListExtractor,
    "llvm/registers/blocks": BlockRegistersListExtractor,
    "llvm/patches/stackframes": PatchesOfStackFramesListExtractor,
    "llvm/patches/bindings": PatchesOfBindingsListExtractor,
    "llvm/patches/callsites": PatchesOfCallsitesListExtractor,
    "llvm/patches/snapshots": PatchesOfSnapshotsListExtractor,
    "llvm/patches/clobbers": PatchesOfClobbersListExtractor,
    "assembler/instructions": InstructionsListExtractor,
}
