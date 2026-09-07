from i13c.core.result import Err, Ok
from i13c.graph.nodes import run as run_graph
from i13c.semantic.graph import SemanticGraph
from i13c.semantic.nodes.resolutions.mnemonics import (
    INSTRUCTIONS_TABLE,
    MnemonicVariant,
)
from i13c.semantic.typing.analyses.llvm import NOP
from i13c.semantic.typing.analyses.blocklets import BlockletInstruction
from i13c.semantic.typing.resolutions.mnemonics import MnemonicOperandSymbol
from i13c.semantic.typing.resolutions.instructions import (
    InstructionAcceptance,
    InstructionRejection,
)
from i13c.syntax.lexing import tokenize
from i13c.syntax.parsing import parse
from i13c.syntax.source import open_text


def parse_table(table: str) -> list[tuple[str, bytes | None]]:
    rows: list[tuple[str, bytes | None]] = []
    lines = [line.strip("|\n ") for line in table.splitlines()[2:-1]]
    headers = [h.strip().lower() for h in lines[0].split("|")]

    assert headers[0] == "instruction"
    assert headers[1] == "encoding"

    try:
        separator = headers.index("***")
    except ValueError:
        separator = len(headers)

    if separator < len(headers):
        assert headers[separator + 1] == "instruction"
        assert headers[separator + 2] == "encoding"

    for line in [line for line in lines[2:] if "---" not in line]:
        parts = [p.strip() for p in line.split("|")]
        left, right = parts[:separator], parts[separator + 1 :]

        for line in [left] if separator == len(headers) else [left, right]:
            assert len(line) == 2

            if "!!" in line[1]:
                rows.append((line[0], None))
            else:
                rows.append((line[0], bytes.fromhex(line[1]) if line[1] else None))

    return rows


def compile(instruction: str) -> SemanticGraph:
    source = open_text(f"""
        asm main() noreturn {{
            {instruction};
        }}
    """)

    match tokenize(source):
        case Err(diagnostics):
            assert False, f"Tokenization failed: {diagnostics}"
        case Ok(tokens):
            tokenized = tokens

    match parse(source, tokenized):
        case Err(diagnostics):
            assert False, f"Parsing failed: {diagnostics}"
        case Ok(_program):
            program = _program

    graph = run_graph(program)
    return graph.semantic_graph()


def encode(table: str):
    for instruction, encoding in parse_table(table):

        try:
            semantic = compile(instruction)
            message = f"Encoding mismatch for instruction: {instruction}"
        except AssertionError:
            assert False, f"Compilation failed for instruction: {instruction}"

        # wrong instruction stopped at resolver won't reach section data
        if encoding is None and semantic.analyses.sections is None:
            continue

        assert semantic.analyses.sections is not None, message
        assert semantic.analyses.sections.size() == 1, message

        _, section = semantic.analyses.sections.peek()

        if encoding is None:
            assert section.data.hex(" ") == "", message

        else:
            assert len(section.data) > 0, message
            assert section.data.hex(" ") == encoding.hex(" "), message


def expand(symbol: MnemonicOperandSymbol) -> tuple[str, ...]:
    # fmt: off
    reg64 = (
        "rax", "rcx", "rdx", "rbx", "rsp", "rbp", "rsi", "rdi",
        "r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15",
    )

    reg32 = (
        "eax", "ecx", "edx", "ebx", "esp", "ebp", "esi", "edi",
        "r8d", "r9d", "r10d", "r11d", "r12d", "r13d", "r14d", "r15d",
    )

    reg16 = (
        "ax", "cx", "dx", "bx", "sp", "bp", "si", "di",
        "r8w", "r9w", "r10w", "r11w", "r12w", "r13w", "r14w", "r15w",
    )

    reg8 = (
        "al", "cl", "dl", "bl", "spl", "bpl", "sil", "dil",
        "r8b", "r9b", "r10b", "r11b", "r12b", "r13b", "r14b", "r15b",
        "ah", "ch", "dh", "bh",
    )

    imm8 = (
        "0x00", "0x01", "0x7f", "0x80", "0xff",
    )

    imm16 = (
        "0x0000", "0x0001", "0x007f", "0x0080", "0x00ff",
        "0x0100", "0x7fff", "0x8000", "0xffff",
    )

    imm32 = (
        "0x00000000", "0x00000001", "0x0000007f", "0x00000080", "0x000000ff", "0x00000100",
        "0x00007fff", "0x00008000", "0x0000ffff", "0x00010000", "0x7fffffff", "0x80000000",
        "0xffffffff",
    )

    imm64 = (
        "0x0000000000000000", "0x0000000000000001", "0x000000000000007f", "0x0000000000000080", "0x00000000000000ff", "0x0000000000000100",
        "0x0000000000007fff", "0x0000000000008000", "0x000000000000ffff", "0x0000000000010000", "0x000000007fffffff", "0x0000000080000000",
        "0x00000000ffffffff", "0x0000000100000000", "0x7fffffffffffffff", "0x8000000000000000", "0xffffffffffffffff",
    )
    # fmt: on

    match symbol:
        case "reg64":
            return reg64

        case "reg32":
            return reg32

        case "reg16":
            return reg16

        case "reg8":
            return reg8

        case "imm8":
            return imm8

        case "imm16":
            return imm16

        case "imm32":
            return imm32

        case "imm64":
            return imm64

        case "rel":
            return ("@prev5", "@prev1", "@next1", "@next5")

        case ("addr8" | "addr16" | "addr32" | "addr64") as symbol:
            scales = (1, 2, 4, 8)
            indexes = tuple(register for register in reg64 if register != "rsp")
            cases: list[str] = []

            match symbol:
                case "addr8":
                    size = "byte"
                case "addr16":
                    size = "word"
                case "addr32":
                    size = "dword"
                case "addr64":
                    size = "qword"

            # every base through ModRM or mandatory SIB
            cases.extend(f"{size} [{base}]" for base in reg64)

            # every SIB base, implicit scale 1
            cases.extend(f"{size} [{base} + 1 * rcx]" for base in reg64)

            # every legal SIB index, implicit scale 1
            cases.extend(f"{size} [rax + 1 * {index}]" for index in indexes)

            # explicit scale field, ordinary registers
            cases.extend(f"{size} [rax + {scale} * rcx]" for scale in scales)

            # explicit scale with REX.B and REX.X
            cases.extend(f"{size} [r8 + {scale} * r9]" for scale in scales)

            # index without a base: mandatory SIB disp32
            cases.extend(f"{size} [{scale} * rcx]" for scale in scales)

            # extended index without a base
            cases.extend(f"{size} [{scale} * r9]" for scale in scales)

            # special index/base interactions
            cases.extend(
                [
                    f"{size} [r13 + 8 * r12]",
                    f"{size} [rsp + 4 * r15]",
                ]
            )

            displacements = (
                "+ 0x00",
                "- 0x00",
                "+ 0x01",
                "- 0x01",
                "+ 0x00000001",
                "- 0x00000001",
                "+ 0x7f",
                "- 0x7f",
                "+ 0x80",
                "- 0x80",
                "- 0x81",
                "+ 0xff",
                "- 0xff",
                "+ 0x7fffffff",
                "- 0x7fffffff",
                "- 0x80000000",
            )

            # displacement cases through SIB
            cases.extend(
                f"{size} [rax + 1 * rcx {displacement}]"
                for displacement in displacements
            )

            # boundary cases without SIB
            cases.extend(
                (
                    f"{size} [r10 + 0x7f]",
                    f"{size} [r10 + 0x80]",
                    f"{size} [r10 - 0x80]",
                    f"{size} [r10 - 0x81]",
                )
            )

            # relative addressing cases
            cases.extend([
                f"{size} [rel @prev5]",
                f"{size} [rel @prev1]",
                f"{size} [rel @next1]",
                f"{size} [rel @next5]",
            ])

            # ordered de-duplication
            return tuple(dict.fromkeys(cases))

    return ()


def cover(domains: list[tuple[str, ...]]) -> tuple[tuple[str, ...], ...]:
    if not domains:
        return ((),)

    rows: dict[tuple[str, ...], None] = {}

    # different baseline value for each operand position.
    baseline = tuple(
        domain[position % len(domain)] for position, domain in enumerate(domains)
    )
    rows[baseline] = None

    # every value appears in every applicable operand position.
    for position, domain in enumerate(domains):
        for value in domain:
            row = list(baseline)
            row[position] = value
            rows[tuple(row)] = None

    # add mixed combinations, including extended/extended registers.
    count = max(len(domain) for domain in domains)

    for index in range(count):
        row = tuple(
            domain[(index + position) % len(domain)]
            for position, domain in enumerate(domains)
        )
        rows[row] = None

    return tuple(rows)


def exhaust(*tables: str):
    visited: set[MnemonicVariant] = set()
    variants: list[MnemonicVariant] = []

    for table in tables:
        variant: MnemonicVariant | None = None
        combinations: list[tuple[str, ...]] = []

        for instruction, _ in parse_table(table):
            semantic = compile(instruction)
            accepted: list[InstructionAcceptance] | None = None
            rejected: list[InstructionRejection] | None = None

            # all instructions must have their resolutions available
            assert semantic.resolutions.instructions is not None

            if semantic.resolutions.instructions.size() == 1:
                _, resolved = semantic.resolutions.instructions.peek()
                accepted, rejected = resolved.accepted, resolved.rejected

            else:
                for resolved in semantic.resolutions.instructions.values():
                    if (
                        resolved.accepted
                        and resolved.accepted[0].mnemonic.name != b"nop"
                    ):
                        accepted, rejected = resolved.accepted, resolved.rejected
                        break

            assert accepted is not None
            assert rejected is not None

            assert len(accepted) == 1

            mnemonic = accepted[0].mnemonic
            variants = INSTRUCTIONS_TABLE[mnemonic.name]

            visited.add(accepted[0].variant)
            variant = accepted[0].variant
            combinations: list[tuple[str, ...]] = []

            for operand in variant:
                combinations.append(
                    tuple(name.decode() for name in operand.names or [])
                    or expand(operand.symbol)
                )

            break

        assert variant is not None
        assert combinations is not None

        found: set[str] = set()
        expected = {":".join(entry) for entry in cover(combinations)}
        rejections: int = 0

        for instruction, _ in parse_table(table):
            semantic = compile(instruction)
            accepted: list[InstructionAcceptance] | None = None
            rejected: list[InstructionRejection] | None = None

            if semantic.resolutions.instructions is None:
                continue

            # all instructions must have their resolutions available
            assert semantic.resolutions.instructions is not None

            if semantic.resolutions.instructions.size() == 1:
                _, resolved = semantic.resolutions.instructions.peek()
                accepted, rejected = resolved.accepted, resolved.rejected

            else:
                for resolved in semantic.resolutions.instructions.values():
                    if (
                        resolved.accepted
                        and resolved.accepted[0].mnemonic.name != b"nop"
                    ):
                        accepted, rejected = resolved.accepted, resolved.rejected
                        break

            assert accepted is not None
            assert rejected is not None

            if accepted:
                assert len(accepted) == 1
                assert id(variant) == id(accepted[0].variant)

            elif rejected:
                rejections += 1
                assert len(rejected) == 1
                assert id(variant) == id(rejected[0].variant)

            if accepted:
                assert semantic.analyses.blocklets is not None
                assert semantic.analyses.blocklets.size() == 1

                _, blocklet = semantic.analyses.blocklets.peek()
                instructions: list[BlockletInstruction] = []

                before: list[BlockletInstruction] = []
                after: list[BlockletInstruction] | None = None

                for block in blocklet.blocks:
                    for instruction in block.instructions:
                        instructions.append(instruction)

                if len(instructions) > 1:
                    for instruction in list(instructions):
                        if isinstance(instruction, NOP):
                            instructions.remove(instruction)

                            if after is not None:
                                after.append(instruction)
                            else:
                                before.append(instruction)

                        else:
                            print("Encountered non-NOP instruction:", instruction)
                            after = []

                assert len(instructions) == 1

                after = after or []
                operands = ":".join(
                    [str(operand) for operand in instructions[0].operands]
                )

                operands = operands.replace("#0", f"@prev{len(before)}")
                operands = operands.replace("#1", f"@next{len(after)-1}")

                found.add(operands)

        # ensure all found instructions are part of the expected set
        assert expected.intersection(found) == found

        # remaining instructions that were expected but were rejected
        difference = expected.difference(found)
        assert len(difference) == rejections

    assert visited == set(variants)
