from collections.abc import Iterable
from dataclasses import dataclass

from i13c.core.diagnostics import Diagnostic
from i13c.core.mapping import OneToMany, OneToOne
from i13c.semantic.typing.analyses.asmlets import Asmlet
from i13c.semantic.typing.analyses.core import AnalysisNodes
from i13c.semantic.typing.entities import EntityNodes
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.entities.parameters import ParameterId
from i13c.semantic.typing.entities.signatures import SignatureId
from i13c.semantic.typing.entities.snippets import SnippetId
from i13c.semantic.typing.entities.statements import StatementId
from i13c.semantic.typing.resolutions.binds import BindAcceptance
from i13c.semantic.typing.resolutions.callsites import CallSiteAcceptance
from i13c.semantic.typing.resolutions.core import ResolutionNodes
from i13c.semantic.typing.resolutions.environments import EnvironmentAcceptance
from i13c.semantic.typing.resolutions.signatures import SignatureAcceptance
from i13c.semantic.typing.resolutions.values import ValueAcceptance


@dataclass
class IndexEdges:
    binds_by_parameters: OneToOne[ParameterId, BindAcceptance] | None
    environments_by_snippets: OneToOne[SnippetId, EnvironmentAcceptance] | None
    signatures_by_names: OneToMany[bytes, SignatureAcceptance] | None
    values_by_statements: OneToMany[StatementId, ValueAcceptance] | None
    callsites_by_signatures: OneToMany[SignatureId, CallSiteAcceptance] | None
    asmlets_by_signatures: OneToMany[SignatureId, Asmlet] | None


@dataclass(kw_only=True)
class SemanticGraph:
    analyses: AnalysisNodes
    entities: EntityNodes
    indices: IndexEdges
    resolutions: ResolutionNodes

    def find_function_by_name(self, name: bytes) -> FunctionId | None:
        for _, _ in self.entities.functions.items():
            pass

        return None


@dataclass(kw_only=True)
class SemanticRules:
    data: dict[str, list[Diagnostic]]

    def count(self) -> int:
        return sum(len(diags) for diags in self.data.values())

    def get(self, name: str) -> list[Diagnostic]:
        return self.data.get(f"rules/{name}", [])

    def enumerate(self) -> Iterable[Diagnostic]:
        for diags in self.data.values():
            yield from diags
