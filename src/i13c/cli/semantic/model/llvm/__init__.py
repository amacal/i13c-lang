from typing import Any, Dict

from i13c.cli.semantic.model.abstract import AbstractListExtractor
from i13c.cli.semantic.model.llvm.blocks import (
    BlockInstructionsListExtractor,
    BlockListExtractor,
)

LLVM: Dict[str, AbstractListExtractor[Any]] = {
    "llvm/blocks": BlockListExtractor,
    "llvm/blocks/instructions": BlockInstructionsListExtractor,
}
