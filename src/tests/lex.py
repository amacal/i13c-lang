import pytest

from i13c import lex, src


def can_tokenize_few_tokens():
    text = "0x1a2f,hello;"
    code = src.open_text(text)

    tokens = lex.tokenize(code)
    assert tokens is not None
    assert len(tokens) == 5

    assert tokens[0] == lex.Token(code=lex.TOKEN_HEX, offset=0, length=6)
    assert tokens[1] == lex.Token(code=lex.TOKEN_COMMA, offset=6, length=1)
    assert tokens[2] == lex.Token(code=lex.TOKEN_IDENT, offset=7, length=5)
    assert tokens[3] == lex.Token(code=lex.TOKEN_SEMICOLON, offset=12, length=1)
    assert tokens[4] == lex.Token(code=lex.TOKEN_EOF, offset=13, length=0)

    assert code.extract(tokens[0]) == b"0x1a2f"
    assert code.extract(tokens[1]) == b","
    assert code.extract(tokens[2]) == b"hello"
    assert code.extract(tokens[3]) == b";"
    assert code.extract(tokens[4]) == b""


def can_tokenize_new_lines():
    text = ";  ;;  "
    code = src.open_text(text)

    tokens = lex.tokenize(code)
    assert tokens is not None
    assert len(tokens) == 4

    assert tokens[0] == lex.Token(code=lex.TOKEN_SEMICOLON, offset=0, length=1)
    assert tokens[1] == lex.Token(code=lex.TOKEN_SEMICOLON, offset=3, length=1)
    assert tokens[2] == lex.Token(code=lex.TOKEN_SEMICOLON, offset=4, length=1)
    assert tokens[3] == lex.Token(code=lex.TOKEN_EOF, offset=7, length=0)

    assert code.extract(tokens[0]) == b";"
    assert code.extract(tokens[1]) == b";"
    assert code.extract(tokens[2]) == b";"
    assert code.extract(tokens[3]) == b""


def can_tokenize_last_hex():
    text = "0xabcdef"
    code = src.open_text(text)

    tokens = lex.tokenize(code)
    assert tokens is not None
    assert len(tokens) == 2

    assert tokens[0] == lex.Token(code=lex.TOKEN_HEX, offset=0, length=8)
    assert tokens[1] == lex.Token(code=lex.TOKEN_EOF, offset=8, length=0)

    assert code.extract(tokens[0]) == b"0xabcdef"
    assert code.extract(tokens[1]) == b""


def can_tokenize_last_ident():
    text = "abcdef"
    code = src.open_text(text)

    tokens = lex.tokenize(code)
    assert tokens is not None
    assert len(tokens) == 2

    assert tokens[0] == lex.Token(code=lex.TOKEN_IDENT, offset=0, length=6)
    assert tokens[1] == lex.Token(code=lex.TOKEN_EOF, offset=6, length=0)

    assert code.extract(tokens[0]) == b"abcdef"
    assert code.extract(tokens[1]) == b""


def can_tokenize_registers():
    text = "mov r15, 0x1234"
    code = src.open_text(text)

    tokens = lex.tokenize(code)
    assert tokens is not None
    assert len(tokens) == 5

    assert tokens[0] == lex.Token(code=lex.TOKEN_IDENT, offset=0, length=3)
    assert tokens[1] == lex.Token(code=lex.TOKEN_REG, offset=4, length=3)
    assert tokens[2] == lex.Token(code=lex.TOKEN_COMMA, offset=7, length=1)
    assert tokens[3] == lex.Token(code=lex.TOKEN_HEX, offset=9, length=6)
    assert tokens[4] == lex.Token(code=lex.TOKEN_EOF, offset=15, length=0)

    assert code.extract(tokens[0]) == b"mov"
    assert code.extract(tokens[1]) == b"r15"
    assert code.extract(tokens[2]) == b","
    assert code.extract(tokens[3]) == b"0x1234"
    assert code.extract(tokens[4]) == b""


def can_omit_whitespaces():
    text = "  0xff  test  "
    code = src.open_text(text)

    tokens = lex.tokenize(code)
    assert tokens is not None
    assert len(tokens) == 3

    assert tokens[0] == lex.Token(code=lex.TOKEN_HEX, offset=2, length=4)
    assert tokens[1] == lex.Token(code=lex.TOKEN_IDENT, offset=8, length=4)
    assert tokens[2] == lex.Token(code=lex.TOKEN_EOF, offset=14, length=0)

    assert code.extract(tokens[0]) == b"0xff"
    assert code.extract(tokens[1]) == b"test"
    assert code.extract(tokens[2]) == b""


def can_detect_hex_with_invalid_characters():
    text = "0x1g"
    code = src.open_text(text)

    with pytest.raises(lex.UnexpectedValue):
        lex.tokenize(code)


def can_detect_too_short_hex():
    text = "0x"
    code = src.open_text(text)

    with pytest.raises(lex.UnexpectedValue):
        lex.tokenize(code)


def can_detect_incomplete_hex():
    text = "0"
    code = src.open_text(text)

    with pytest.raises(lex.UnexpectedEndOfFile):
        lex.tokenize(code)


def can_detect_ident_followed_by_invalid_character():
    text = "hello-xab"
    code = src.open_text(text)

    with pytest.raises(lex.UnexpectedValue):
        lex.tokenize(code)
