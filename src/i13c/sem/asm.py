from dataclasses import dataclass
from typing import Dict, List
from typing import Literal as Kind
from typing import Optional, Tuple, Union

from i13c import ast
from i13c.sem.core import Width, derive_width
from i13c.sem.syntax import SyntaxGraph
from i13c.src import Span


@dataclass(kw_only=True)
class Register:
    name: bytes

    def __str__(self) -> str:
        return self.name.decode()


@dataclass(kw_only=True)
class Immediate:
    value: int
    width: Optional[Width]


@dataclass(kw_only=True)
class Reference:
    name: bytes


BindingKind = Kind[b"register", b"immediate"]


@dataclass(kw_only=True)
class Binding:
    kind: BindingKind
    name: bytes

    @staticmethod
    def register(name: bytes) -> "Binding":
        return Binding(kind=b"register", name=name)

    @staticmethod
    def immediate() -> "Binding":
        return Binding(kind=b"immediate", name=b"imm")

    def __str__(self) -> str:
        return self.name.decode()


@dataclass(kw_only=True)
class Mnemonic:
    name: bytes


OperandKind = Kind[b"register", b"immediate", b"reference"]
OperandTarget = Union[Register, Immediate, Reference]


@dataclass(kw_only=True, frozen=True)
class OperandId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("operand", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Operand:
    kind: OperandKind
    target: OperandTarget

    @staticmethod
    def register(name: bytes) -> Operand:
        return Operand(kind=b"register", target=Register(name=name))

    @staticmethod
    def immediate(value: int) -> Operand:
        return Operand(
            kind=b"immediate", target=Immediate(value=value, width=derive_width(value))
        )

    @staticmethod
    def reference(name: bytes) -> Operand:
        return Operand(kind=b"reference", target=Reference(name=name))

    def describe(self) -> str:
        return self.kind[0:3].decode()


@dataclass(kw_only=True, frozen=True)
class InstructionId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("instruction", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Instruction:
    ref: Span
    mnemonic: Mnemonic
    operands: List[OperandId]

    def describe(self) -> str:
        operands = ":".join(op.identify(2) for op in self.operands)
        return f"mnemonic={self.mnemonic.name.decode():<8} operands={operands}"


@dataclass(kw_only=True, frozen=True)
class OperandSpec:
    kind: OperandKind
    width: Optional[Width]

    def __str__(self) -> str:
        return f"{self.kind.decode()}:({self.width})"

    @staticmethod
    def register() -> "OperandSpec":
        return OperandSpec(kind=b"register", width=64)

    @staticmethod
    def immediate(width: Width) -> "OperandSpec":
        return OperandSpec(kind=b"immediate", width=width)

    def describe(self) -> str:
        return self.kind[0:3].decode()


MnemonicBindings = List[Union[Register, Immediate]]


@dataclass(kw_only=True)
class Acceptance:
    mnemonic: Mnemonic
    variant: MnemonicVariant
    bindings: MnemonicBindings

    def describe(self) -> str:
        variants = ":".join(var.describe() for var in self.variant)
        return f"mnemonic={self.mnemonic.name.decode():<8} variants={variants}"


RejectionReason = Kind[
    b"wrong-arity",
    b"type-mismatch",
    b"width-mismatch",
    b"unresolved",
]


@dataclass(kw_only=True)
class Rejection:
    mnemonic: Mnemonic
    variant: MnemonicVariant
    reason: RejectionReason


@dataclass(kw_only=True)
class Resolution:
    accepted: List[Acceptance]
    rejected: List[Rejection]

    def describe(self) -> str:
        candidate = ""

        if len(self.accepted) > 0:
            candidate = self.accepted[0].describe()

        return (
            f"accepted={len(self.accepted)} rejected={len(self.rejected)} {candidate}"
        )


MnemonicVariant = Tuple[OperandSpec, ...]


@dataclass(kw_only=True)
class OperandRejection:
    pass


OperandAcceptanceKind = Kind[b"register", b"immediate"]
OperandAcceptanceTarget = Union[Register, Immediate]


@dataclass(kw_only=True)
class OperandAcceptance:
    kind: OperandAcceptanceKind
    target: OperandAcceptanceTarget

    def describe(self) -> str:
        return f"kind={self.kind} target={self.target}"


@dataclass(kw_only=True)
class OperandResolution:
    accepted: List[OperandAcceptance]
    rejected: List[OperandRejection]

    def describe(self) -> str:
        candidate = ""

        if len(self.accepted) > 0:
            candidate = self.accepted[0].describe()

        return (
            f"accepted={len(self.accepted)} rejected={len(self.rejected)} {candidate}"
        )


INSTRUCTIONS_TABLE: Dict[bytes, List[MnemonicVariant]] = {
    b"syscall": [()],
    b"mov": [
        (OperandSpec.register(), OperandSpec.immediate(64)),
        (OperandSpec.register(), OperandSpec.immediate(32)),
        (OperandSpec.register(), OperandSpec.immediate(16)),
        (OperandSpec.register(), OperandSpec.immediate(8)),
    ],
    b"shl": [
        (OperandSpec.register(), OperandSpec.immediate(8)),
    ],
}


def match_operand(operand: Operand, spec: OperandSpec) -> Optional[RejectionReason]:

    if operand.kind != spec.kind:
        return b"type-mismatch"

    if operand.kind == b"register":
        assert isinstance(operand.target, Register)

        if spec.width != 64:
            return b"width-mismatch"

    if operand.kind == b"immediate":
        assert isinstance(operand.target, Immediate)

        if operand.target.width != spec.width:
            return b"width-mismatch"

    return None


def match_instruction(
    operands: Dict[OperandId, Operand],
    resolutions: Dict[OperandId, OperandResolution],
    instruction: Instruction,
    variants: List[MnemonicVariant],
) -> Tuple[
    Dict[MnemonicVariant, MnemonicBindings], Dict[MnemonicVariant, RejectionReason]
]:

    accepted: Dict[MnemonicVariant, MnemonicBindings] = {}
    rejected: Dict[MnemonicVariant, RejectionReason] = {}

    for variant in variants:
        reason: Optional[RejectionReason] = None

        # first check arity
        if len(instruction.operands) != len(variant):
            rejected[variant] = b"wrong-arity"
            continue

        # then check each operand
        for oid, spec in zip(instruction.operands, variant):

            # take provided operand
            operand: Operand = operands[oid]

            # if operand is a reference, try to resolve
            # but take only first acceptance, because
            # ambiguity will be reported elsewhere
            if operand.kind == b"reference":
                if oid in resolutions:
                    if resolved := resolutions[oid].accepted:
                        operand = Operand(
                            kind=resolved[0].kind,
                            target=resolved[0].target,
                        )

            # any reason requires immediate stop
            if reason := match_operand(operand, spec):
                break

        # finally, classify as accepted or rejected
        if reason is None:
            accepted[variant] = []
        else:
            rejected[variant] = reason

    return accepted, rejected


def build_instructions(
    graph: SyntaxGraph,
) -> Dict[InstructionId, Instruction]:
    instructions: Dict[InstructionId, Instruction] = {}

    for nid, instruction in graph.instructions.items():
        operands: List[OperandId] = []

        # collect operand IDs from reverse mapping
        for operand in instruction.operands:
            oid = graph.operands.get_by_node(operand)
            operands.append(OperandId(value=oid.value))

        # derive instruction ID from globally unique node ID
        instruction_id = InstructionId(value=nid.value)

        # append to instructions map
        instructions[instruction_id] = Instruction(
            ref=instruction.ref,
            mnemonic=Mnemonic(name=instruction.mnemonic.name),
            operands=operands,
        )

    return instructions


def build_operands(
    graph: SyntaxGraph,
) -> Dict[OperandId, Operand]:
    operands: Dict[OperandId, Operand] = {}

    for nid, operand in graph.operands.items():
        match operand:
            case ast.Register() as reg:
                target = Operand.register(name=reg.name)
            case ast.Immediate() as imm:
                target = Operand.immediate(value=imm.value)
            case ast.Reference() as ref:
                target = Operand.reference(name=ref.name)

        # derive operand ID from globally unique node ID
        operand_id = OperandId(value=nid.value)

        # append to operands map
        operands[operand_id] = target

    return operands


def build_resolutions(
    operands: Dict[OperandId, Operand],
    instructions: Dict[InstructionId, Instruction],
    resolution_by_operand: Dict[OperandId, OperandResolution],
) -> Dict[InstructionId, Resolution]:
    resolutions: Dict[InstructionId, Resolution] = {}

    for iid, instruction in instructions.items():
        accepted: Dict[MnemonicVariant, MnemonicBindings] = {}
        rejected: Dict[MnemonicVariant, RejectionReason] = {}

        if variants := INSTRUCTIONS_TABLE.get(instruction.mnemonic.name):
            accepted, rejected = match_instruction(
                operands, resolution_by_operand, instruction, variants
            )

        acceptance = [
            Acceptance(
                mnemonic=instruction.mnemonic, variant=variant, bindings=bindings
            )
            for variant, bindings in accepted.items()
        ]

        rejection = [
            Rejection(mnemonic=instruction.mnemonic, variant=variant, reason=reason)
            for variant, reason in rejected.items()
        ]

        resolutions[iid] = Resolution(
            accepted=acceptance,
            rejected=rejection,
        )

    return resolutions
