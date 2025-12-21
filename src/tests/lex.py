from i13c import lex, src, res


def can_tokenize_few_tokens():
    text = "0x1a2f,hello;"
    code = src.open_text(text)

    tokens = lex.tokenize(code)
    assert tokens is not None

    assert isinstance(tokens, res.Ok)
    assert len(tokens.value) == 5

    assert tokens.value[0] == lex.Token(code=lex.TOKEN_HEX, offset=0, length=6)
    assert tokens.value[1] == lex.Token(code=lex.TOKEN_COMMA, offset=6, length=1)
    assert tokens.value[2] == lex.Token(code=lex.TOKEN_IDENT, offset=7, length=5)
    assert tokens.value[3] == lex.Token(code=lex.TOKEN_SEMICOLON, offset=12, length=1)
    assert tokens.value[4] == lex.Token(code=lex.TOKEN_EOF, offset=13, length=0)

    assert code.extract(tokens.value[0]) == b"0x1a2f"
    assert code.extract(tokens.value[1]) == b","
    assert code.extract(tokens.value[2]) == b"hello"
    assert code.extract(tokens.value[3]) == b";"
    assert code.extract(tokens.value[4]) == b""


def can_tokenize_new_lines():
    text = ";  ;;  "
    code = src.open_text(text)

    tokens = lex.tokenize(code)
    assert tokens is not None

    assert isinstance(tokens, res.Ok)
    assert len(tokens.value) == 4

    assert tokens.value[0] == lex.Token(code=lex.TOKEN_SEMICOLON, offset=0, length=1)
    assert tokens.value[1] == lex.Token(code=lex.TOKEN_SEMICOLON, offset=3, length=1)
    assert tokens.value[2] == lex.Token(code=lex.TOKEN_SEMICOLON, offset=4, length=1)
    assert tokens.value[3] == lex.Token(code=lex.TOKEN_EOF, offset=7, length=0)

    assert code.extract(tokens.value[0]) == b";"
    assert code.extract(tokens.value[1]) == b";"
    assert code.extract(tokens.value[2]) == b";"
    assert code.extract(tokens.value[3]) == b""


def can_tokenize_last_hex():
    text = "0xabcdef"
    code = src.open_text(text)

    tokens = lex.tokenize(code)
    assert tokens is not None

    assert isinstance(tokens, res.Ok)
    assert len(tokens.value) == 2

    assert tokens.value[0] == lex.Token(code=lex.TOKEN_HEX, offset=0, length=8)
    assert tokens.value[1] == lex.Token(code=lex.TOKEN_EOF, offset=8, length=0)

    assert code.extract(tokens.value[0]) == b"0xabcdef"
    assert code.extract(tokens.value[1]) == b""


def can_tokenize_last_ident():
    text = "abcdef"
    code = src.open_text(text)

    tokens = lex.tokenize(code)
    assert tokens is not None

    assert isinstance(tokens, res.Ok)
    assert len(tokens.value) == 2

    assert tokens.value[0] == lex.Token(code=lex.TOKEN_IDENT, offset=0, length=6)
    assert tokens.value[1] == lex.Token(code=lex.TOKEN_EOF, offset=6, length=0)

    assert code.extract(tokens.value[0]) == b"abcdef"
    assert code.extract(tokens.value[1]) == b""


def can_tokenize_registers():
    text = "mov r15, 0x1234"
    code = src.open_text(text)

    tokens = lex.tokenize(code)
    assert tokens is not None

    assert isinstance(tokens, res.Ok)
    assert len(tokens.value) == 5

    assert tokens.value[0] == lex.Token(code=lex.TOKEN_IDENT, offset=0, length=3)
    assert tokens.value[1] == lex.Token(code=lex.TOKEN_REG, offset=4, length=3)
    assert tokens.value[2] == lex.Token(code=lex.TOKEN_COMMA, offset=7, length=1)
    assert tokens.value[3] == lex.Token(code=lex.TOKEN_HEX, offset=9, length=6)
    assert tokens.value[4] == lex.Token(code=lex.TOKEN_EOF, offset=15, length=0)

    assert code.extract(tokens.value[0]) == b"mov"
    assert code.extract(tokens.value[1]) == b"r15"
    assert code.extract(tokens.value[2]) == b","
    assert code.extract(tokens.value[3]) == b"0x1234"
    assert code.extract(tokens.value[4]) == b""


def can_omit_whitespaces():
    text = "  0xff  test  "
    code = src.open_text(text)

    tokens = lex.tokenize(code)
    assert tokens is not None

    assert isinstance(tokens, res.Ok)
    assert len(tokens.value) == 3

    assert tokens.value[0] == lex.Token(code=lex.TOKEN_HEX, offset=2, length=4)
    assert tokens.value[1] == lex.Token(code=lex.TOKEN_IDENT, offset=8, length=4)
    assert tokens.value[2] == lex.Token(code=lex.TOKEN_EOF, offset=14, length=0)

    assert code.extract(tokens.value[0]) == b"0xff"
    assert code.extract(tokens.value[1]) == b"test"
    assert code.extract(tokens.value[2]) == b""


def can_detect_unrecognized_token():
    code = src.open_text("@")
    tokens = lex.tokenize(code)

    assert isinstance(tokens, res.Err)
    diagnostics = tokens.error

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.offset == 0
    assert diagnostic.code == "L001"


def can_detect_hex_with_invalid_characters():
    code = src.open_text("0x1g")
    tokens = lex.tokenize(code)

    assert isinstance(tokens, res.Err)
    diagnostics = tokens.error

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.offset == 3
    assert diagnostic.code == "L003"


def can_detect_too_short_hex():
    code = src.open_text("0x")

    tokens = lex.tokenize(code)

    assert isinstance(tokens, res.Err)
    diagnostics = tokens.error

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.offset == 2
    assert diagnostic.code == "L003"


def can_detect_incomplete_hex():
    code = src.open_text("0")
    tokens = lex.tokenize(code)

    assert isinstance(tokens, res.Err)
    diagnostics = tokens.error

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.offset == 1
    assert diagnostic.code == "L002"


def can_detect_ident_followed_by_invalid_character():
    code = src.open_text("hello-xab")
    tokens = lex.tokenize(code)

    assert isinstance(tokens, res.Err)
    diagnostics = tokens.error

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.offset == 5
    assert diagnostic.code == "L003"
