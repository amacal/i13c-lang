from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional

from i13c.core.diagnostics import Diagnostic
from i13c.core.mapping import OneToMany, OneToOne
from i13c.semantic.typing.entities import EntityNodes
from i13c.semantic.typing.entities.asmlets import Asmlet
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.entities.parameters import ParameterId
from i13c.semantic.typing.entities.signatures import SignatureId
from i13c.semantic.typing.entities.snippets import SnippetId
from i13c.semantic.typing.entities.statements import StatementId
from i13c.semantic.typing.resolutions import ResolutionNodes
from i13c.semantic.typing.resolutions.binds import BindAcceptance
from i13c.semantic.typing.resolutions.callsites import CallSiteAcceptance
from i13c.semantic.typing.resolutions.environments import EnvironmentAcceptance
from i13c.semantic.typing.resolutions.signatures import SignatureAcceptance
from i13c.semantic.typing.resolutions.values import ValueAcceptance


@dataclass
class IndexEdges:
    binds_by_parameters: Optional[OneToOne[ParameterId, BindAcceptance]]
    environments_by_snippets: Optional[OneToOne[SnippetId, EnvironmentAcceptance]]
    signatures_by_names: Optional[OneToMany[bytes, SignatureAcceptance]]
    values_by_statements: Optional[OneToMany[StatementId, ValueAcceptance]]
    callsites_by_signatures: Optional[OneToMany[SignatureId, CallSiteAcceptance]]
    asmlets_by_signatures: Optional[OneToMany[SignatureId, Asmlet]]


@dataclass(kw_only=True)
class SemanticGraph:
    entities: EntityNodes
    indices: IndexEdges
    resolutions: ResolutionNodes

    def find_function_by_name(self, name: bytes) -> Optional[FunctionId]:
        for _, _ in self.entities.functions.items():
            pass
            # if function.identifier.data == name:
            #     return fid

        return None


@dataclass(kw_only=True)
class SemanticRules:
    data: Dict[str, List[Diagnostic]]

    def count(self) -> int:
        return sum(len(diags) for diags in self.data.values())

    def get(self, name: str) -> List[Diagnostic]:
        return self.data.get(f"rules/{name}", [])

    def enumerate(self) -> Iterable[Diagnostic]:
        for diags in self.data.values():
            yield from diags
