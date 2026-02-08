from dataclasses import dataclass
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Protocol,
    Tuple,
    TypeVar,
)

import click

from i13c import lex, par, src
from i13c.cli import unwrap
from i13c.cli.semantic.model.entities.callsites import CallSiteListExtractor
from i13c.cli.semantic.model.entities.expressions import ExpressionListExtractor
from i13c.cli.semantic.model.entities.functions import FunctionListExtractor
from i13c.cli.semantic.model.entities.instructions import InstructionListExtractor
from i13c.cli.semantic.model.entities.literals import LiteralListExtractor
from i13c.cli.semantic.model.entities.operands import OperandListExtractor
from i13c.cli.semantic.model.entities.parameters import ParameterListExtractor
from i13c.cli.semantic.model.entities.snippets import SnippetListExtractor
from i13c.cli.semantic.model.entities.variables import VariableListExtractor
from i13c.cli.semantic.model.indices.controlflows import ControlFlowListExtractor
from i13c.cli.semantic.model.indices.dataflows import DataFlowListExtractor
from i13c.cli.semantic.model.indices.instances import InstanceListExtractor
from i13c.cli.semantic.model.indices.resolutions import (
    CallSiteResolutionListExtractor,
    InstructionResolutionListExtractor,
)
from i13c.cli.semantic.model.indices.terminalities import TerminalityListExtractor
from i13c.cli.semantic.model.indices.variables import ParameterVariablesListExtractor
from i13c.core.mapping import Descriptive, Identified
from i13c.core.table import Table, draw_table
from i13c.sem.model import SemanticGraph, build_semantic_graph
from i13c.sem.syntax import build_syntax_graph

ListItem = TypeVar("ListItem")


class AbstractListExtractor(Protocol[ListItem]):
    @staticmethod
    def headers() -> Dict[str, str]: ...

    @staticmethod
    def extract(graph: SemanticGraph) -> Iterable[ListItem]: ...

    @staticmethod
    def rows(entry: ListItem) -> Dict[str, str]: ...


def draw_list(
    extractor: AbstractListExtractor[ListItem], graph: SemanticGraph
) -> Table:
    entries = extractor.extract(graph)
    rows = [extractor.rows(entry) for entry in entries]

    return draw_table(extractor.headers(), rows)


class Showable(Protocol):
    def show(self) -> Iterable[str]: ...


SemanticId = TypeVar("SemanticId", covariant=True)
SemanticNode = TypeVar("SemanticNode", covariant=True)


class OneToOneLike(Protocol[SemanticId, SemanticNode]):
    def items(self) -> Iterable[Tuple[SemanticId, SemanticNode]]: ...


class OneToManyLike(Protocol[SemanticId, SemanticNode]):
    def items(self) -> Iterable[Tuple[SemanticId, Iterable[SemanticNode]]]: ...


ExtractOneToOne = Callable[[SemanticGraph], OneToOneLike[Identified, Descriptive]]
ExtractOneToMany = Callable[[SemanticGraph], OneToManyLike[Identified, Descriptive]]


@dataclass(kw_only=True)
class OneToOneFeature:
    list: Optional[Callable[[SemanticGraph], OneToOneLike[Identified, Descriptive]]] = (
        None
    )
    show: Optional[Callable[[SemanticGraph], OneToOneLike[Identified, Showable]]] = None


ENTITIES: Dict[str, AbstractListExtractor[Any]] = {
    "entities/functions": FunctionListExtractor,
    "entities/callsites": CallSiteListExtractor,
    "entities/expressions": ExpressionListExtractor,
    "entities/instructions": InstructionListExtractor,
    "entities/literals": LiteralListExtractor,
    "entities/operands": OperandListExtractor,
    "entities/parameters": ParameterListExtractor,
    "entities/snippets": SnippetListExtractor,
    "entities/variables": VariableListExtractor,
}

INDICES: Dict[str, AbstractListExtractor[Any]] = {
    "indices/controlflow-by-function": ControlFlowListExtractor,
    "indices/dataflow-by-flownode": DataFlowListExtractor,
    "indices/instance-by-callsite": InstanceListExtractor,
    "indices/resolution-by-callsite": CallSiteResolutionListExtractor,
    "indices/resolution-by-instruction": InstructionResolutionListExtractor,
    "indices/variables-by-parameter": ParameterVariablesListExtractor,
    "indices/terminality-by-function": TerminalityListExtractor,
}


def list_one2one_semantic(
    extractor: AbstractListExtractor[Any], model: SemanticGraph
) -> None:
    for line in draw_list(extractor, model).entries:
        click.echo(line)


def show_one2one_semantic(
    nodes: OneToOneLike[Identified, Showable], node_id: int
) -> None:
    for id, node in nodes.items():
        if id.value == node_id:
            click.echo(f"{id.identify(2)}")
            for line in node.show():
                click.echo(f"  {line}")


def load_model(path: str) -> SemanticGraph:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    code = src.open_text(text)
    tokens = unwrap(lex.tokenize(code), source=code)
    program = unwrap(par.parse(code, tokens), source=code)
    graph = build_syntax_graph(program)
    model = build_semantic_graph(graph)

    return model


def attach_one2one_commands(
    target: click.Group, node: str, extractor: AbstractListExtractor[Any]
) -> List[click.Command]:

    # introduce a sub-command group for each semantic mapping
    @target.group(node)
    def group() -> None:
        pass

    @group.command("list")
    @click.argument("path", type=click.Path(exists=True))
    def list(path: str) -> None:
        # if extract.list is not None:
        list_one2one_semantic(extractor, load_model(path))

    return [list]


def attach(target: click.Group) -> List[click.Command]:
    commands: List[click.Command] = []

    @target.group("model")
    def model() -> None:
        pass

    for key, extractor in ENTITIES.items():
        commands.extend(attach_one2one_commands(model, key, extractor))

    for key, extractor in INDICES.items():
        commands.extend(attach_one2one_commands(model, key, extractor))

    return commands
