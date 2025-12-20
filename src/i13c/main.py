import click

from i13c import lex, par, src


@click.group()
def i13c():
    pass


@i13c.command("tokenize")
@click.argument("path", type=click.Path(exists=True))
def tokenize_command(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    code = src.open_text(text)
    tokens = lex.tokenize(code)

    for token in tokens:
        key = f"{token.code:03}:{token.offset:04}:{token.length:02}"
        value = code.extract(token)

        click.echo(f"{key} -> {value!r}")


@i13c.command("parse")
@click.argument("path", type=click.Path(exists=True))
def parse_command(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    code = src.open_text(text)
    tokens = lex.tokenize(code)
    program = par.parse(code, tokens)

    for instruction in program.instructions:
        operands = ", ".join([str(op) for op in instruction.operands])
        click.echo(f"{str(instruction.mnemonic)} {operands}")
