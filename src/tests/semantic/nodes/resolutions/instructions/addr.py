from tests.semantic.nodes.resolutions.instructions import (
    samples,
    verify_instruction_resolution,
)


@samples("""
    | -------------- | -------- | ------------- | -------- | ---------------- |
    | instruction    | mnemonic | variant       | status   | reason           |
    | -------------- | -------- | ------------- | -------- | ---------------- |
    | lea rax, [rbx] | lea      | reg64, addr64 | accepted | -                |
    | lea ecx, [rbx] | lea      | reg32, addr64 | accepted | -                |
    | lea dx, [rbx]  | lea      | reg16, addr64 | accepted | -                |
    | lea rax        | lea      | reg64         | rejected | arity-mismatch   |
    | -------------- | -------- | ------------- | -------- | ---------------- |
""")
def can_handle_lea(
    instruction: str,
    mnemonic: str,
    variant: list[str],
    status: bool,
    reason: str | None,
):
    verify_instruction_resolution(instruction, mnemonic, variant, status, reason)
