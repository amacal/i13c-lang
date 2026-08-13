from collections.abc import Iterable
from typing import Protocol

from i13c.core.generator import Generator
from i13c.core.graph import GraphNode, GraphViews
from i13c.core.mapping import OneToMany, OneToOne
from i13c.semantic.core import Hex
from i13c.semantic.typing.analyses.asmlets import (
    Asmlet,
    AsmletId,
    AsmletInstruction,
    AsmletOperand,
    AsmletOperandAddress,
    AsmletOperandImmediate,
    AsmletOperandRegister,
    AsmletOperandRelocation,
    AsmletOperandTarget,
)
from i13c.semantic.typing.entities.signatures import SignatureId
from i13c.semantic.typing.entities.snippets import SnippetId
from i13c.semantic.typing.resolutions.addresses import AddressAcceptance
from i13c.semantic.typing.resolutions.callsites import CallSiteAcceptance
from i13c.semantic.typing.resolutions.immediates import ImmediateAcceptance
from i13c.semantic.typing.resolutions.instructions import InstructionAcceptance
from i13c.semantic.typing.resolutions.labels import LabelAcceptance
from i13c.semantic.typing.resolutions.literals import LiteralAcceptance
from i13c.semantic.typing.resolutions.operands import OperandAcceptance, OperandTarget
from i13c.semantic.typing.resolutions.parameters import ParameterAcceptance
from i13c.semantic.typing.resolutions.registers import RegisterAcceptance
from i13c.semantic.typing.resolutions.snippets import SnippetAcceptance


def configure_asmlets() -> GraphNode:
    return GraphNode(
        builder=build_asmlets,
        constraint=None,
        produces=("analyses/asmlets",),
        requires=frozenset(
            {
                ("generator", "core/generator"),
                ("callsites", "indices/callsites/signatures"),
                ("snippets", "resolutions/snippets/accepted"),
            }
        ),
        views=GraphViews(list=ListExtractor),
    )


def build_asmlets(
    generator: Generator,
    callsites: OneToMany[SignatureId, CallSiteAcceptance],
    snippets: OneToOne[SnippetId, SnippetAcceptance],
) -> OneToOne[AsmletId, Asmlet]:
    asmlets: dict[AsmletId, Asmlet] = {}

    for sid, snippet in snippets.items():
        removed: list[bytes] = []
        positions: list[bool] = [False] * len(snippet.binding.binds)
        index: dict[frozenset[tuple[bytes, Hex]], list[CallSiteAcceptance]] = {}

        for idx, bind in enumerate(snippet.binding.binds):
            if bind.is_immediate():
                removed.append(bind.src)
            else:
                positions[idx] = True

        for callsite in callsites.find(snippet.signature.id):
            keys: list[tuple[bytes, Hex]] = []

            for idx, (bind, argument) in enumerate(
                zip(snippet.binding.binds, callsite.arguments)
            ):
                if not positions[idx]:
                    assert isinstance(argument, LiteralAcceptance)
                    keys.append((bind.src, argument.target))

            if frozenset(keys) not in index:
                index[frozenset(keys)] = [callsite]
            else:
                index[frozenset(keys)].append(callsite)

            if len(index[frozenset(keys)]) > 1:
                continue

            # copy all binds except those that are immediate
            binds = [bind for bind in snippet.binding.binds if bind.src not in removed]

            # copy all parameters except those that are immediate
            parameters = [
                param
                for param in snippet.signature.parameters
                if param.name not in removed
            ]

            # mapping of parameter name to bind source for all register parameters
            mapping: dict[bytes, bytes | Hex] = {
                bind.src: bind.dst for bind in binds
            }

            # append all immediate arguments
            for entry in keys:
                mapping[entry[0]] = entry[1]

            # rewrite all instructions to replace any immediate binds with the callsite argument
            instructions = [
                rewrite_instruction(instr, mapping) for instr in snippet.instructions
            ]

            # generate new identifier for the asmlet
            aid = AsmletId(value=generator.next())

            asmlets[aid] = Asmlet(
                ref=snippet.ref,
                id=aid,
                source=sid,
                noreturn=snippet.noreturn,
                keys=dict(keys),
                signature=snippet.signature,
                name=snippet.signature.name,
                callsites=index[frozenset(keys)],
                binding=binds,
                parameters=parameters,
                instructions=instructions,
            )

    return OneToOne[AsmletId, Asmlet].instance(asmlets)


def register_converter(
    ctx: InstructionAcceptance,
    src: RegisterAcceptance,
    binds: dict[bytes, bytes | Hex],
) -> AsmletOperandRegister:
    return AsmletOperandRegister(name=src.name)


def immediate_converter(
    ctx: InstructionAcceptance,
    src: ImmediateAcceptance,
    binds: dict[bytes, bytes | Hex],
) -> AsmletOperandImmediate:
    return AsmletOperandImmediate(value=src.value)


def label_converter(
    ctx: InstructionAcceptance,
    src: LabelAcceptance,
    binds: dict[bytes, bytes | Hex],
) -> AsmletOperandRelocation:
    return AsmletOperandRelocation(offset=src.index - ctx.index)


def parameter_converter(
    ctx: InstructionAcceptance,
    src: ParameterAcceptance,
    binds: dict[bytes, bytes | Hex],
) -> AsmletOperandRegister | AsmletOperandImmediate:

    # the parameter resolved to a value via binds
    value = binds[src.name]

    # either directly to an immediate value
    if isinstance(value, Hex):
        return AsmletOperandImmediate(value=value)

    # or to a register that can be used as an operand
    else:
        return AsmletOperandRegister(name=value)


def address_converter(
    ctx: InstructionAcceptance,
    src: AddressAcceptance,
    binds: dict[bytes, bytes | Hex],
) -> AsmletOperandAddress:

    # the base of an address can only be a register
    if isinstance(src.base, RegisterAcceptance):
        base = AsmletOperandRegister(name=src.base.name)

    # or a referenced register via binds
    else:
        value = binds[src.base.name]
        assert not isinstance(value, Hex)
        base = AsmletOperandRegister(name=value)

    # displacement is optional
    if src.offset is not None:
        displacement = src.offset.value.value
    else:
        displacement = None

    return AsmletOperandAddress(
        base=base,
        displacement=displacement,
    )


class OperandConverter(Protocol):
    def __call__(
        self,
        ctx: InstructionAcceptance,
        src: OperandTarget,
        binds: dict[bytes, bytes | Hex],
    ) -> AsmletOperandTarget: ...


DISPATCH_TABLE: dict[type[OperandTarget], OperandConverter] = {
    AddressAcceptance: address_converter,
    ImmediateAcceptance: immediate_converter,
    LabelAcceptance: label_converter,
    ParameterAcceptance: parameter_converter,
    RegisterAcceptance: register_converter,
}  # pyright: ignore[reportAssignmentType]


def rewrite_operand(
    ctx: InstructionAcceptance,
    src: OperandAcceptance,
    binds: dict[bytes, bytes | Hex],
) -> AsmletOperand:
    return AsmletOperand(
        ref=src.ref,
        symbol=src.symbol,
        target=DISPATCH_TABLE[type(src.target)](ctx, src.target, binds),
    )


def rewrite_instruction(
    src: InstructionAcceptance,
    binds: dict[bytes, bytes | Hex],
) -> AsmletInstruction:
    return AsmletInstruction(
        ref=src.ref,
        id=src.id,
        mnemonic=src.mnemonic.name,
        operands=[rewrite_operand(src, op, binds) for op in src.operands],
    )


class ListExtractor:
    def __init__(self, data: OneToOne[AsmletId, Asmlet]):
        self.data = data

    def extract(self) -> Iterable[tuple[AsmletId, Asmlet]]:
        yield from self.data.items()

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "src": "Source",
            "sig": "Signature",
            "name": "Name",
            "keys": "Keys",
            "parameters": "Parameters",
            "callsites": "Callsites",
            "instructions": "Instructions",
        }

    @staticmethod
    def rows(key: AsmletId, entry: Asmlet) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "src": entry.source.identify(1),
            "sig": entry.signature.id.identify(1),
            "name": entry.name.decode(),
            "keys": ", ".join(f"{key.decode()}:{value}" for key, value in entry.keys.items()),
            "parameters": ", ".join(str(param) for param in entry.parameters),
            "callsites": str(len(entry.callsites)),
            "instructions": str(len(entry.instructions)),
        }
