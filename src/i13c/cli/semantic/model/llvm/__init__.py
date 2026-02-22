from typing import Any, Dict

from i13c.cli.semantic.model.abstract import AbstractListExtractor
from i13c.cli.semantic.model.llvm.blocks import (
    BlockInstructionsListExtractor,
    BlockListExtractor,
)
from i13c.cli.semantic.model.llvm.functions import (
    EntriesListExtractor,
    ExitsListExtractor,
)
from i13c.cli.semantic.model.llvm.instructions import InstructionsListExtractor
from i13c.cli.semantic.model.llvm.registers import RegistersListExtractor

LLVM: Dict[str, AbstractListExtractor[Any]] = {
    "llvm/blocks": BlockListExtractor,
    "llvm/blocks/instructions": BlockInstructionsListExtractor,
    "llvm/instructions": InstructionsListExtractor,
    "llvm/functions/entries": EntriesListExtractor,
    "llvm/functions/exits": ExitsListExtractor,
    "llvm/registers": RegistersListExtractor,
}
