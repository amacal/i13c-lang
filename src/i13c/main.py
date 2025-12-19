import click

from i13c import lex


@click.group()
def i13c():
    pass


@i13c.command()
@click.argument("path", type=click.Path(exists=True))
def tokenize(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    lexer = lex.open_text(text)
    tokens = lex.tokenize(lexer)

    for token in tokens:
        key = f"{token.code:03}:{token.offset:04}:{token.length:02}"
        value = lexer.extract(token)

        click.echo(f"{key} -> {value!r}")
