from i13c.core import result
from i13c.syntax.lexing import Token, Tokens, tokenize
from i13c.syntax.source import open_text


def can_tokenize_few_tokens():
    text = "0x1a2f,hello;"
    code = open_text(text)

    tokens = tokenize(code)
    assert tokens is not None

    assert isinstance(tokens, result.Ok)
    assert len(tokens.value) == 5

    assert tokens.value[0] == Token(code=Tokens.HEX, offset=0, length=6)
    assert tokens.value[1] == Token(code=Tokens.COMMA, offset=6, length=1)
    assert tokens.value[2] == Token(code=Tokens.IDENT, offset=7, length=5)
    assert tokens.value[3] == Token(code=Tokens.SEMICOLON, offset=12, length=1)
    assert tokens.value[4] == Token(code=Tokens.EOF, offset=13, length=0)

    assert code.extract(tokens.value[0]) == b"0x1a2f"
    assert code.extract(tokens.value[1]) == b","
    assert code.extract(tokens.value[2]) == b"hello"
    assert code.extract(tokens.value[3]) == b";"
    assert code.extract(tokens.value[4]) == b""


def can_tokenize_new_lines():
    text = ";  ;;  "
    code = open_text(text)

    tokens = tokenize(code)
    assert tokens is not None

    assert isinstance(tokens, result.Ok)
    assert len(tokens.value) == 4

    assert tokens.value[0] == Token(code=Tokens.SEMICOLON, offset=0, length=1)
    assert tokens.value[1] == Token(code=Tokens.SEMICOLON, offset=3, length=1)
    assert tokens.value[2] == Token(code=Tokens.SEMICOLON, offset=4, length=1)
    assert tokens.value[3] == Token(code=Tokens.EOF, offset=7, length=0)

    assert code.extract(tokens.value[0]) == b";"
    assert code.extract(tokens.value[1]) == b";"
    assert code.extract(tokens.value[2]) == b";"
    assert code.extract(tokens.value[3]) == b""


def can_reject_windows_line_endings():
    text = ";  ;;\r\n  "
    code = open_text(text)

    tokens = tokenize(code)
    assert tokens is not None

    assert isinstance(tokens, result.Err)
    assert len(tokens.error) == 1

    diagnostic = tokens.error[0]
    assert diagnostic.code == "E1000"
    assert code.extract(diagnostic.ref) == b"\r"

    assert diagnostic.ref.offset == 5
    assert diagnostic.ref.length == 1


def can_tokenize_single_bytes():
    text = ";,}{)(:@][=+-"
    code = open_text(text)

    tokens = tokenize(code)
    assert tokens is not None

    assert isinstance(tokens, result.Ok)
    assert len(tokens.value) == 14

    assert tokens.value[0] == Token(code=Tokens.SEMICOLON, offset=0, length=1)
    assert tokens.value[1] == Token(code=Tokens.COMMA, offset=1, length=1)
    assert tokens.value[2] == Token(code=Tokens.CURLY_CLOSE, offset=2, length=1)
    assert tokens.value[3] == Token(code=Tokens.CURLY_OPEN, offset=3, length=1)
    assert tokens.value[4] == Token(code=Tokens.ROUND_CLOSE, offset=4, length=1)
    assert tokens.value[5] == Token(code=Tokens.ROUND_OPEN, offset=5, length=1)
    assert tokens.value[6] == Token(code=Tokens.COLON, offset=6, length=1)
    assert tokens.value[7] == Token(code=Tokens.AT, offset=7, length=1)
    assert tokens.value[8] == Token(code=Tokens.SQUARE_CLOSE, offset=8, length=1)
    assert tokens.value[9] == Token(code=Tokens.SQUARE_OPEN, offset=9, length=1)
    assert tokens.value[10] == Token(code=Tokens.EQUALS, offset=10, length=1)
    assert tokens.value[11] == Token(code=Tokens.PLUS, offset=11, length=1)
    assert tokens.value[12] == Token(code=Tokens.MINUS, offset=12, length=1)
    assert tokens.value[13] == Token(code=Tokens.EOF, offset=13, length=0)

    assert code.extract(tokens.value[0]) == b";"
    assert code.extract(tokens.value[1]) == b","
    assert code.extract(tokens.value[2]) == b"}"
    assert code.extract(tokens.value[3]) == b"{"
    assert code.extract(tokens.value[4]) == b")"
    assert code.extract(tokens.value[5]) == b"("
    assert code.extract(tokens.value[6]) == b":"
    assert code.extract(tokens.value[7]) == b"@"
    assert code.extract(tokens.value[8]) == b"]"
    assert code.extract(tokens.value[9]) == b"["
    assert code.extract(tokens.value[10]) == b"="
    assert code.extract(tokens.value[11]) == b"+"
    assert code.extract(tokens.value[12]) == b"-"
    assert code.extract(tokens.value[13]) == b""


def can_tokenize_dot_operator():
    text = "0x12.0x20"
    code = open_text(text)

    tokens = tokenize(code)
    assert tokens is not None

    assert isinstance(tokens, result.Ok)
    assert len(tokens.value) == 4

    assert tokens.value[0] == Token(code=Tokens.HEX, offset=0, length=4)
    assert tokens.value[1] == Token(code=Tokens.DOT, offset=4, length=1)
    assert tokens.value[2] == Token(code=Tokens.HEX, offset=5, length=4)
    assert tokens.value[3] == Token(code=Tokens.EOF, offset=9, length=0)

    assert code.extract(tokens.value[0]) == b"0x12"
    assert code.extract(tokens.value[1]) == b"."
    assert code.extract(tokens.value[2]) == b"0x20"
    assert code.extract(tokens.value[3]) == b""


def can_tokenize_range_operator():
    text = "0x12..0x20"
    code = open_text(text)

    tokens = tokenize(code)
    assert tokens is not None

    assert isinstance(tokens, result.Ok)
    assert len(tokens.value) == 4

    assert tokens.value[0] == Token(code=Tokens.HEX, offset=0, length=4)
    assert tokens.value[1] == Token(code=Tokens.RANGE, offset=4, length=2)
    assert tokens.value[2] == Token(code=Tokens.HEX, offset=6, length=4)
    assert tokens.value[3] == Token(code=Tokens.EOF, offset=10, length=0)

    assert code.extract(tokens.value[0]) == b"0x12"
    assert code.extract(tokens.value[1]) == b".."
    assert code.extract(tokens.value[2]) == b"0x20"
    assert code.extract(tokens.value[3]) == b""


def can_tokenize_range_operator_with_spaces():
    text = "0x12  ..   0x20"
    code = open_text(text)

    tokens = tokenize(code)
    assert tokens is not None

    assert isinstance(tokens, result.Ok)
    assert len(tokens.value) == 4

    assert tokens.value[0] == Token(code=Tokens.HEX, offset=0, length=4)
    assert tokens.value[1] == Token(code=Tokens.RANGE, offset=6, length=2)
    assert tokens.value[2] == Token(code=Tokens.HEX, offset=11, length=4)
    assert tokens.value[3] == Token(code=Tokens.EOF, offset=15, length=0)

    assert code.extract(tokens.value[0]) == b"0x12"
    assert code.extract(tokens.value[1]) == b".."
    assert code.extract(tokens.value[2]) == b"0x20"
    assert code.extract(tokens.value[3]) == b""


def can_tokenize_last_hex():
    text = "0xabcdef"
    code = open_text(text)

    tokens = tokenize(code)
    assert tokens is not None

    assert isinstance(tokens, result.Ok)
    assert len(tokens.value) == 2

    assert tokens.value[0] == Token(code=Tokens.HEX, offset=0, length=8)
    assert tokens.value[1] == Token(code=Tokens.EOF, offset=8, length=0)

    assert code.extract(tokens.value[0]) == b"0xabcdef"
    assert code.extract(tokens.value[1]) == b""


def can_tokenize_last_ident():
    text = "abcdef"
    code = open_text(text)

    tokens = tokenize(code)
    assert tokens is not None

    assert isinstance(tokens, result.Ok)
    assert len(tokens.value) == 2

    assert tokens.value[0] == Token(code=Tokens.IDENT, offset=0, length=6)
    assert tokens.value[1] == Token(code=Tokens.EOF, offset=6, length=0)

    assert code.extract(tokens.value[0]) == b"abcdef"
    assert code.extract(tokens.value[1]) == b""


def can_tokenize_registers():
    text = "mov r15, 0x1234"
    code = open_text(text)

    tokens = tokenize(code)
    assert tokens is not None

    assert isinstance(tokens, result.Ok)
    assert len(tokens.value) == 5

    assert tokens.value[0] == Token(code=Tokens.IDENT, offset=0, length=3)
    assert tokens.value[1] == Token(code=Tokens.IDENT, offset=4, length=3)
    assert tokens.value[2] == Token(code=Tokens.COMMA, offset=7, length=1)
    assert tokens.value[3] == Token(code=Tokens.HEX, offset=9, length=6)
    assert tokens.value[4] == Token(code=Tokens.EOF, offset=15, length=0)

    assert code.extract(tokens.value[0]) == b"mov"
    assert code.extract(tokens.value[1]) == b"r15"
    assert code.extract(tokens.value[2]) == b","
    assert code.extract(tokens.value[3]) == b"0x1234"
    assert code.extract(tokens.value[4]) == b""


def can_tokenize_mnemonics():
    text = "syscall mov"
    code = open_text(text)

    tokens = tokenize(code)
    assert tokens is not None

    assert isinstance(tokens, result.Ok)
    assert len(tokens.value) == 3

    assert tokens.value[0] == Token(code=Tokens.IDENT, offset=0, length=7)
    assert tokens.value[1] == Token(code=Tokens.IDENT, offset=8, length=3)
    assert tokens.value[2] == Token(code=Tokens.EOF, offset=11, length=0)

    assert code.extract(tokens.value[0]) == b"syscall"
    assert code.extract(tokens.value[1]) == b"mov"
    assert code.extract(tokens.value[2]) == b""


def can_tokenize_keywords():
    text = "asm mov clobbers noreturn fn imm"
    code = open_text(text)

    tokens = tokenize(code)
    assert tokens is not None

    assert isinstance(tokens, result.Ok)
    assert len(tokens.value) == 7

    assert tokens.value[0] == Token(code=Tokens.KEYWORD, offset=0, length=3)
    assert tokens.value[1] == Token(code=Tokens.IDENT, offset=4, length=3)
    assert tokens.value[2] == Token(code=Tokens.KEYWORD, offset=8, length=8)
    assert tokens.value[3] == Token(code=Tokens.KEYWORD, offset=17, length=8)
    assert tokens.value[4] == Token(code=Tokens.KEYWORD, offset=26, length=2)
    assert tokens.value[5] == Token(code=Tokens.KEYWORD, offset=29, length=3)
    assert tokens.value[6] == Token(code=Tokens.EOF, offset=32, length=0)

    assert code.extract(tokens.value[0]) == b"asm"
    assert code.extract(tokens.value[1]) == b"mov"
    assert code.extract(tokens.value[2]) == b"clobbers"
    assert code.extract(tokens.value[3]) == b"noreturn"
    assert code.extract(tokens.value[4]) == b"fn"
    assert code.extract(tokens.value[5]) == b"imm"
    assert code.extract(tokens.value[6]) == b""


def can_omit_whitespaces():
    text = "  0xff  test  "
    code = open_text(text)

    tokens = tokenize(code)
    assert tokens is not None

    assert isinstance(tokens, result.Ok)
    assert len(tokens.value) == 3

    assert tokens.value[0] == Token(code=Tokens.HEX, offset=2, length=4)
    assert tokens.value[1] == Token(code=Tokens.IDENT, offset=8, length=4)
    assert tokens.value[2] == Token(code=Tokens.EOF, offset=14, length=0)

    assert code.extract(tokens.value[0]) == b"0xff"
    assert code.extract(tokens.value[1]) == b"test"
    assert code.extract(tokens.value[2]) == b""


def can_detect_unrecognized_token():
    code = open_text("\xff")
    tokens = tokenize(code)

    assert isinstance(tokens, result.Err)
    diagnostics = tokens.error

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.ref.offset == 0
    assert diagnostic.ref.length == 1
    assert diagnostic.code == "E1000"


def can_detect_hex_with_invalid_characters():
    code = open_text("0x1g")
    tokens = tokenize(code)

    assert isinstance(tokens, result.Err)
    diagnostics = tokens.error

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.ref.offset == 3
    assert diagnostic.ref.length == 1
    assert diagnostic.code == "E1002"


def can_detect_too_short_hex_when_eof():
    code = open_text("0x")
    tokens = tokenize(code)

    assert isinstance(tokens, result.Err)
    diagnostics = tokens.error

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.ref.offset == 2
    assert diagnostic.ref.length == 1
    assert diagnostic.code == "E1001"


def can_detect_too_long_hex():
    code = open_text("0x0011223344556677889")
    tokens = tokenize(code)

    assert isinstance(tokens, result.Err)
    diagnostics = tokens.error

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.ref.offset == 0
    assert diagnostic.ref.length == 19
    assert diagnostic.code == "E1003"


def can_reject_hex_without_digits():
    code = open_text("0x;")
    tokens = tokenize(code)

    assert isinstance(tokens, result.Err)
    diagnostics = tokens.error

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.ref.offset == 2
    assert diagnostic.ref.length == 1
    assert diagnostic.code == "E1002"


def can_detect_incomplete_hex():
    code = open_text("0")
    tokens = tokenize(code)

    assert isinstance(tokens, result.Err)
    diagnostics = tokens.error

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.ref.offset == 1
    assert diagnostic.ref.length == 1
    assert diagnostic.code == "E1001"


def can_reject_ident_followed_by_invalid_character():
    code = open_text("hello`xab")
    tokens = tokenize(code)

    assert isinstance(tokens, result.Err)
    diagnostics = tokens.error

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.ref.offset == 5
    assert diagnostic.ref.length == 1
    assert diagnostic.code == "E1002"
