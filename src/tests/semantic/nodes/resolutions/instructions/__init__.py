from collections.abc import Callable, Iterable, Sequence
from typing import Any

from pytest import mark

from i13c.graph.nodes import run as run_graph
from i13c.semantic.typing.resolutions.instructions import InstructionResolution
from tests.semantic import prepare_program


def parse_value(header: str, value: str) -> str | bool | list[str] | None:
    if not value.strip(" -"):
        return None

    if header in ("variant"):
        return [v.strip() for v in value.split(",")]

    if header in ("status"):
        return value.strip() == "accepted"

    return value


def parse_samples(
    table: str,
) -> tuple[Sequence[str], Iterable[Sequence[str | bool | list[str] | None]]]:
    rows: list[Sequence[str | bool | list[str] | None]] = []
    lines = [line.strip("|\n ") for line in table.strip().splitlines()[1:-1]]
    headers = [h.strip().lower() for h in lines[0].split("|")]

    try:
        separator = headers.index("***")
    except ValueError:
        separator = len(headers)

    for line in [line for line in lines[2:] if "---" not in line]:
        parts = [p.strip() for p in line.split("|")]
        left, right = parts[:separator], parts[separator + 1 :]

        rows.append([parse_value(headers[i], left[i]) for i in range(separator)])

        if separator < len(parts):
            rows.append([parse_value(headers[i], right[i]) for i in range(separator)])

    return (headers[:separator], rows)


def samples(table: str):
    def wrapper(fn: Callable[..., Any]) -> Callable[..., Any]:
        headers, cases = parse_samples(table)
        return mark.parametrize(",".join(headers), cases)(fn)

    return wrapper


def prepare_resolution(code: str) -> InstructionResolution:
    _, program = prepare_program(code)
    semantic = run_graph(program).semantic_graph()

    assert semantic.resolutions.instructions is not None
    assert semantic.resolutions.instructions.size() == 1
    _, value = semantic.resolutions.instructions.peek()

    return value


def verify_instruction_resolution(
    instruction: str,
    mnemonic: str,
    variant: list[str],
    status: bool,
    reason: str | None,
):
    resolution = prepare_resolution(
        f"""
            asm main() {{ .x: {instruction}; }}
        """
    )

    assert len(resolution.rejected) >= (0 if status else 1)
    assert len(resolution.accepted) >= (1 if status else 0)

    if status:
        acceptance = resolution.accepted[0]

        assert acceptance.mnemonic.name == mnemonic.encode()
        assert len(acceptance.variant) == len(variant or [])

        if variant:
            assert list(map(str, acceptance.variant)) == variant

    if reason:
        assert any(str(d.reason) == reason for d in resolution.rejected), f"Expected reason: {reason}"
