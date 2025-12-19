import pytest

from i13c import lex


def can_tokenize_few_tokens():
    text = "0x1a2f,hello\n"
    lexer = lex.open_text(text)

    tokens = lex.tokenize(lexer)
    assert tokens is not None
    assert len(tokens) == 5

    assert tokens[0] == lex.Token(code=lex.TOKEN_HEX, offset=0, length=6)
    assert tokens[1] == lex.Token(code=lex.TOKEN_COMMA, offset=6, length=1)
    assert tokens[2] == lex.Token(code=lex.TOKEN_IDENT, offset=7, length=5)
    assert tokens[3] == lex.Token(code=lex.TOKEN_NEWLINE, offset=12, length=1)
    assert tokens[4] == lex.Token(code=lex.TOKEN_EOF, offset=13, length=0)

    assert lexer.extract(tokens[0]) == b"0x1a2f"
    assert lexer.extract(tokens[1]) == b","
    assert lexer.extract(tokens[2]) == b"hello"
    assert lexer.extract(tokens[3]) == b"\n"
    assert lexer.extract(tokens[4]) == b""


def can_tokenize_new_lines():
    text = "\n  \n\n  "
    lexer = lex.open_text(text)

    tokens = lex.tokenize(lexer)
    assert tokens is not None
    assert len(tokens) == 4

    assert tokens[0] == lex.Token(code=lex.TOKEN_NEWLINE, offset=0, length=1)
    assert tokens[1] == lex.Token(code=lex.TOKEN_NEWLINE, offset=3, length=1)
    assert tokens[2] == lex.Token(code=lex.TOKEN_NEWLINE, offset=4, length=1)
    assert tokens[3] == lex.Token(code=lex.TOKEN_EOF, offset=7, length=0)

    assert lexer.extract(tokens[0]) == b"\n"
    assert lexer.extract(tokens[1]) == b"\n"
    assert lexer.extract(tokens[2]) == b"\n"
    assert lexer.extract(tokens[3]) == b""


def can_tokenize_last_hex():
    text = "0xabcdef"
    lexer = lex.open_text(text)

    tokens = lex.tokenize(lexer)
    assert tokens is not None
    assert len(tokens) == 2

    assert tokens[0] == lex.Token(code=lex.TOKEN_HEX, offset=0, length=8)
    assert tokens[1] == lex.Token(code=lex.TOKEN_EOF, offset=8, length=0)

    assert lexer.extract(tokens[0]) == b"0xabcdef"
    assert lexer.extract(tokens[1]) == b""


def can_tokenize_last_ident():
    text = "abcdef"
    lexer = lex.open_text(text)

    tokens = lex.tokenize(lexer)
    assert tokens is not None
    assert len(tokens) == 2

    assert tokens[0] == lex.Token(code=lex.TOKEN_IDENT, offset=0, length=6)
    assert tokens[1] == lex.Token(code=lex.TOKEN_EOF, offset=6, length=0)

    assert lexer.extract(tokens[0]) == b"abcdef"
    assert lexer.extract(tokens[1]) == b""


def can_tokenize_registers():
    text = "mov r15, 0x1234"
    lexer = lex.open_text(text)

    tokens = lex.tokenize(lexer)
    assert tokens is not None
    assert len(tokens) == 5

    assert tokens[0] == lex.Token(code=lex.TOKEN_IDENT, offset=0, length=3)
    assert tokens[1] == lex.Token(code=lex.TOKEN_REG, offset=4, length=3)
    assert tokens[2] == lex.Token(code=lex.TOKEN_COMMA, offset=7, length=1)
    assert tokens[3] == lex.Token(code=lex.TOKEN_HEX, offset=9, length=6)
    assert tokens[4] == lex.Token(code=lex.TOKEN_EOF, offset=15, length=0)

    assert lexer.extract(tokens[0]) == b"mov"
    assert lexer.extract(tokens[1]) == b"r15"
    assert lexer.extract(tokens[2]) == b","
    assert lexer.extract(tokens[3]) == b"0x1234"
    assert lexer.extract(tokens[4]) == b""


def can_omit_whitespaces():
    text = "  0xff  test  "
    lexer = lex.open_text(text)

    tokens = lex.tokenize(lexer)
    assert tokens is not None
    assert len(tokens) == 3

    assert tokens[0] == lex.Token(code=lex.TOKEN_HEX, offset=2, length=4)
    assert tokens[1] == lex.Token(code=lex.TOKEN_IDENT, offset=8, length=4)
    assert tokens[2] == lex.Token(code=lex.TOKEN_EOF, offset=14, length=0)

    assert lexer.extract(tokens[0]) == b"0xff"
    assert lexer.extract(tokens[1]) == b"test"
    assert lexer.extract(tokens[2]) == b""


def can_detect_hex_with_invalid_characters():
    text = "0x1g"
    lexer = lex.open_text(text)

    with pytest.raises(lex.UnexpectedValue):
        lex.tokenize(lexer)


def can_detect_too_short_hex():
    text = "0x"
    lexer = lex.open_text(text)

    with pytest.raises(lex.UnexpectedValue):
        lex.tokenize(lexer)


def can_detect_incomplete_hex():
    text = "0"
    lexer = lex.open_text(text)

    with pytest.raises(lex.UnexpectedEndOfFile):
        lex.tokenize(lexer)


def can_detect_ident_followed_by_invalid_character():
    text = "hello-xab"
    lexer = lex.open_text(text)

    with pytest.raises(lex.UnexpectedValue):
        lex.tokenize(lexer)
