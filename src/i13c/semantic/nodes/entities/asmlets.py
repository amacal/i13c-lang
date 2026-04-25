from typing import Dict, FrozenSet, List, Protocol, Tuple, Type, Union

from i13c.core.generator import Generator
from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToMany, OneToOne
from i13c.semantic.core import Hex
from i13c.semantic.typing.entities.asmlets import (
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
from i13c.semantic.typing.resolutions.literals import LiteralAcceptance
from i13c.semantic.typing.resolutions.operands import OperandAcceptance, OperandTarget
from i13c.semantic.typing.resolutions.parameters import ParameterAcceptance
from i13c.semantic.typing.resolutions.references import ReferenceAcceptance
from i13c.semantic.typing.resolutions.registers import RegisterAcceptance
from i13c.semantic.typing.resolutions.snippets import SnippetAcceptance


def configure_asmlets() -> GraphNode:
    return GraphNode(
        builder=build_asmlets,
        constraint=None,
        produces=("entities/asmlets",),
        requires=frozenset(
            {
                ("generator", "core/generator"),
                ("callsites", "indices/callsites/signatures"),
                ("snippets", "resolutions/snippets/accepted"),
            }
        ),
    )


def build_asmlets(
    generator: Generator,
    callsites: OneToMany[SignatureId, CallSiteAcceptance],
    snippets: OneToOne[SnippetId, SnippetAcceptance],
) -> OneToOne[AsmletId, Asmlet]:
    assigns: Dict[AsmletId, Asmlet] = {}

    for sid, snippet in snippets.items():
        removed: List[bytes] = []
        positions: List[bool] = [False] * len(snippet.binding.binds)
        index: Dict[FrozenSet[Tuple[bytes, Hex]], List[CallSiteAcceptance]] = {}

        for idx, bind in enumerate(snippet.binding.binds):
            if bind.is_immediate():
                removed.append(bind.src)
            else:
                positions[idx] = True

        for callsite in callsites.find(snippet.signature.id):
            keys: List[Tuple[bytes, Hex]] = []

            for idx, (bind, argument) in enumerate(zip(snippet.binding.binds, callsite.arguments)):
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

            # copy all paramaters except those that are immediate
            parameters = [
                param
                for param in snippet.signature.parameters
                if param.name not in removed
            ]

            # mapping of parameter name to bind source for all register parameters
            mapping: Dict[bytes, Union[bytes, Hex]] = {
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

            assigns[aid] = Asmlet(
                ref=snippet.ref,
                id=aid,
                source=sid,
                flags=snippet.flags,
                signature=snippet.signature.id,
                name=snippet.signature.name,
                binding=binds,
                parameters=parameters,
                instructions=instructions,
            )

    return OneToOne[AsmletId, Asmlet].instance(assigns)


def register_converter(
    src: RegisterAcceptance,
    binds: Dict[bytes, Union[bytes, Hex]],
) -> AsmletOperandRegister:
    return AsmletOperandRegister(name=src.name)


def immediate_converter(
    src: ImmediateAcceptance,
    binds: Dict[bytes, Union[bytes, Hex]],
) -> AsmletOperandImmediate:
    return AsmletOperandImmediate(value=src.value)


def reference_converter(
    src: ReferenceAcceptance,
    binds: Dict[bytes, Union[bytes, Hex]],
) -> Union[
    AsmletOperandRegister,
    AsmletOperandImmediate,
    AsmletOperandRelocation,
]:

    # target can be resolved as a parameter
    if isinstance(src.target, ParameterAcceptance):
        value = binds[src.target.name]

        # either directly to an immediate value
        if isinstance(value, Hex):
            return AsmletOperandImmediate(value=value)

        # or to a register that can be used as an operand
        else:
            return AsmletOperandRegister(name=value)

    else:
        return AsmletOperandRelocation(offset=-1)


def address_converter(
    src: AddressAcceptance,
    binds: Dict[bytes, Union[bytes, Hex]],
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
        src: OperandTarget,
        binds: Dict[bytes, Union[bytes, Hex]],
    ) -> AsmletOperandTarget: ...


DISPATCH_TABLE: Dict[Type[OperandTarget], OperandConverter] = {
    RegisterAcceptance: register_converter,
    ImmediateAcceptance: immediate_converter,
    ReferenceAcceptance: reference_converter,
    AddressAcceptance: address_converter,
}  # pyright: ignore[reportAssignmentType]


def rewrite_operand(
    src: OperandAcceptance,
    binds: Dict[bytes, Union[bytes, Hex]],
) -> AsmletOperand:
    return AsmletOperand(
        ref=src.ref,
        symbol=src.symbol,
        target=DISPATCH_TABLE[type(src.target)](src.target, binds),
    )


def rewrite_instruction(
    src: InstructionAcceptance,
    binds: Dict[bytes, Union[bytes, Hex]],
) -> AsmletInstruction:
    return AsmletInstruction(
        ref=src.ref,
        id=src.id,
        mnemonic=src.mnemonic.name,
        operands=[rewrite_operand(op, binds) for op in src.operands],
    )
