from dataclasses import dataclass
from typing import Union

from i13c.semantic.typing.resolutions.functions import FunctionAcceptance
from i13c.semantic.typing.resolutions.snippets import SnippetAcceptance

EntrypointTarget = Union[FunctionAcceptance, SnippetAcceptance]


@dataclass(kw_only=True)
class Entrypoint:
    target: EntrypointTarget
