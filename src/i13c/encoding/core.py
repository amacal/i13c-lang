from dataclasses import dataclass


@dataclass(kw_only=True)
class LabelArtifact:
    target: int
    offset: int


@dataclass(kw_only=True)
class RelocationArtifact:
    target: int
    offset: int


class UnreachableEncodingError(Exception):
    pass
