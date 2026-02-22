from typing import Any, Dict

from i13c.cli.semantic.model.abstract import AbstractListExtractor
from i13c.cli.semantic.model.llvm.blocks import (
    BlockInstructionsListExtractor,
    BlockListExtractor,
)
from i13c.cli.semantic.model.llvm.instructions import InstructionsListExtractor

LLVM: Dict[str, AbstractListExtractor[Any]] = {
    "llvm/blocks": BlockListExtractor,
    "llvm/blocks/instructions": BlockInstructionsListExtractor,
    # "llvm/blocks/registers": None,
    # "llvm/blocks/forward": None,
    # "llvm/blocks/backward": None,
    "llvm/instructions": InstructionsListExtractor,
    # "llvm/abstracts": None,
    # "llvm/abstracts/instructions": None,
    # "llvm/flows": None,
    # "llvm/flows/instructions": None,
    # "llvm/function/entries": None,
    # "llvm/function/exits": None,
}
