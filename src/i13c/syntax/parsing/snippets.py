from i13c.syntax import tree
from i13c.syntax.lexing import Token as LexingToken
from i13c.syntax.lexing import Tokens
from i13c.syntax.parsing.core import (
    FlagAlreadySpecified,
    ParsingState,
    UnexpectedKeyword,
)
from i13c.syntax.parsing.literals import extract_hex
from i13c.syntax.parsing.types import parse_range


def parse_snippet(state: ParsingState) -> tree.snippet.Snippet:
    body: list[tree.snippet.InstructionOrLabel] = []
    slots: list[tree.snippet.Slot] = []
    flags: tree.snippet.Flags | None = None

    # snippet name is an identifier
    name = state.expect(Tokens.IDENT)

    # expect opening round bracket
    state.expect(Tokens.ROUND_OPEN)

    # optional snippet parameters
    if not state.is_in(Tokens.ROUND_CLOSE):
        slots = parse_slots(state)

    # expect closed round bracket
    end = state.expect(Tokens.ROUND_CLOSE)

    # optional flags
    if not state.is_in(Tokens.CURLY_OPEN):
        flags = parse_flags(state)

    # expect opening curly brace
    state.expect(Tokens.CURLY_OPEN)

    # parse instructions until closing curly brace
    while not state.is_in(Tokens.CURLY_CLOSE):
        body.append(parse_instruction(state))

    # expect closed curly brace
    state.expect(Tokens.CURLY_CLOSE)

    return tree.snippet.Snippet(
        ref=state.between(name, end),
        signature=tree.snippet.Signature(
            ref=state.between(name, end),
            name=state.extract(name),
            slots=slots,
        ),
        flags=flags,
        body=body,
    )


def parse_slots(state: ParsingState) -> list[tree.snippet.Slot]:
    parameters: list[tree.snippet.Slot] = []
    parameters.append(parse_slot(state))

    # a comma suggests next parameter
    while state.accept(Tokens.COMMA):
        parameters.append(parse_slot(state))

    return parameters


def parse_slot(state: ParsingState) -> tree.snippet.Slot:
    ident = state.expect(Tokens.IDENT)

    # expect '@' followed by ident (register) or immediate
    state.expect(Tokens.AT)
    bind = state.expect(Tokens.IDENT, Tokens.KEYWORD)

    # if it's a keyword, it has to be "imm"
    if bind.code == Tokens.KEYWORD:  # noqa: SIM102
        if state.extract(bind) != b"imm":
            raise UnexpectedKeyword(bind, [b"imm"], state.extract(bind))

    # expect ':' followed by type
    state.expect(Tokens.COLON)
    type = state.expect(Tokens.IDENT)

    if state.is_in(Tokens.SQUARE_OPEN):
        range, end = parse_range(state)
    else:
        range, end = None, type

    return tree.snippet.Slot(
        ref=state.between(ident, end),
        name=state.extract(ident),
        bind=tree.snippet.Bind(
            ref=state.between(bind, bind),
            name=state.extract(bind),
        ),
        type=tree.types.Type(
            ref=state.between(type, end),
            name=state.extract(type),
            range=range,
        ),
    )


def parse_flags(
    state: ParsingState,
) -> tree.snippet.Flags | None:
    keyword: LexingToken | None = None
    start: LexingToken | None = None
    end: LexingToken | None = None

    clobbers: list[tree.snippet.Register] | None = None
    noreturn: bool | None = None

    while not state.is_in(Tokens.CURLY_OPEN):
        expected = {b"clobbers", b"noreturn"}
        keyword = state.expect(Tokens.KEYWORD)

        # set boundaries
        start = start or keyword
        end = keyword

        # fail if the keyword is not "noreturn"
        if state.extract(keyword) not in expected:
            raise UnexpectedKeyword(keyword, expected, state.extract(keyword))

        # if "clobbers", parse the clobber list
        if state.extract(keyword) == b"clobbers":
            if clobbers is not None:
                raise FlagAlreadySpecified(keyword, b"clobbers")
            else:
                clobbers, end = parse_clobbers(state)

        # if "noreturn", set terminal flag
        elif state.extract(keyword) == b"noreturn":
            if noreturn:
                raise FlagAlreadySpecified(keyword, b"noreturn")
            else:
                noreturn = True

    if not start or not end:
        return None

    return tree.snippet.Flags(
        ref=state.between(start, end),
        noreturn=noreturn,
        clobbers=clobbers,
    )


def parse_clobbers(
    state: ParsingState,
) -> tuple[list[tree.snippet.Register], LexingToken]:
    clobbers: list[tree.snippet.Register] = []

    # at least one register is expected
    clobber = state.expect(Tokens.IDENT)
    clobbers.append(
        tree.snippet.Register(
            ref=state.span(clobber),
            name=state.extract(clobber),
        )
    )

    # a comma suggests next clobber
    while state.accept(Tokens.COMMA):
        clobber = state.expect(Tokens.IDENT)
        clobbers.append(
            tree.snippet.Register(
                ref=state.span(clobber),
                name=state.extract(clobber),
            )
        )

    return clobbers, clobber


def parse_instruction(state: ParsingState) -> tree.snippet.InstructionOrLabel:
    operands: list[tree.snippet.Operand] = []
    token = state.expect(Tokens.IDENT, Tokens.DOT)

    # if instruction starts with a dot, it's a label definition
    if token.code == Tokens.DOT:
        return parse_label(state, token)

    # optional operands
    if state.is_in(*OPERANDS_START):
        operands = parse_operands(state)

    # expect a semicolon
    end = state.expect(Tokens.SEMICOLON)

    # build instruction and token reference
    mnemonic = tree.snippet.Mnemonic(
        ref=state.between(token, token),
        name=state.extract(token),
    )

    return tree.snippet.Instruction(
        ref=state.between(token, end),
        mnemonic=mnemonic,
        operands=operands,
    )


def parse_label(state: ParsingState, start: LexingToken) -> tree.snippet.Label:
    # the label name is an identifier
    token = state.expect(Tokens.IDENT)

    # expect a colon
    end = state.expect(Tokens.COLON)

    return tree.snippet.Label(
        ref=state.between(start, end),
        name=state.extract(token),
    )


OPERANDS_START = [Tokens.IDENT, Tokens.HEX, Tokens.AT, Tokens.SQUARE_OPEN]


def parse_operands(state: ParsingState) -> list[tree.snippet.Operand]:
    operands: list[tree.snippet.Operand] = []
    operands.append(parse_operand(state))

    # a comma suggests next operand
    while state.accept(Tokens.COMMA):
        operands.append(parse_operand(state))

    return operands


def parse_operand(state: ParsingState) -> tree.snippet.Operand:
    token = state.expect(*OPERANDS_START)
    operand: tree.snippet.OperandTarget | None = None

    # register has to provide its name
    if token.code == Tokens.IDENT:
        operand = tree.snippet.Register(
            ref=state.between(token, token),
            name=state.extract(token),
        )

    # immediate has to provide its decimal value
    elif token.code == Tokens.HEX:
        operand = tree.snippet.Immediate(
            ref=state.between(token, token),
            data=extract_hex(state, token),
        )

    # reference has to provide its identifier
    elif token.code == Tokens.AT:
        operand = parse_reference(state, token)

    # address operands starts fixed non-registerkeywords
    # so it can really resemble a register operand
    if isinstance(operand, tree.snippet.Register):  # noqa: SIM102
        if operand.name in (b"byte", b"word", b"dword", b"qword"):
            operand = parse_address(state, token)

    if operand is None:
        operand = parse_address(state, token)

    # at this place we have it
    assert operand is not None

    return tree.snippet.Operand(
        ref=operand.ref,
        target=operand,
    )


def parse_address(state: ParsingState, token: LexingToken) -> tree.snippet.Address:
    size: LexingToken | None = None

    # address size if provided
    if token.code == Tokens.IDENT:
        size = token
        token = state.expect(Tokens.SQUARE_OPEN)

    end = state.expect(
        Tokens.IDENT,  # for any register or rip/rel
        Tokens.AT,  # for any reference
        Tokens.DIGIT,  # for any scaler
    )

    if end.code == Tokens.IDENT:
        match state.extract(end):
            case b"rel":
                return parse_address_rel(state, size, token, end)

            case _:
                pass

    return parse_address_base(state, size, token, end)


def parse_address_rel(
    state: ParsingState,
    size: LexingToken | None,
    start: LexingToken,
    end: LexingToken,
) -> tree.snippet.Address:
    # expect the '@' symbol indicating a reference
    token = state.expect(Tokens.AT)

    # parse the reference following the '@' symbol
    reference = parse_reference(state, token)

    # expect the closing square bracket of the address
    end = state.expect(Tokens.SQUARE_CLOSE)

    return tree.snippet.Address(
        ref=state.between(start, end),
        size=size and state.extract(size),
        base=None,
        indx=None,
        disp=reference,
    )


def parse_address_base(
    state: ParsingState,
    size: LexingToken | None,
    start: LexingToken,
    end: LexingToken,
) -> tree.snippet.Address:
    # optionally, a base, an offset or an index can be provided
    base: tree.snippet.Register | tree.snippet.Reference | None = None
    indx: tree.snippet.Index | None = None
    operator: LexingToken | None = None
    displacement: tree.snippet.Displacement | None = None

    while end.code != Tokens.SQUARE_CLOSE:
        # if there's a base (register or reference)
        if base is None and end.code in (Tokens.IDENT, Tokens.AT):
            end, base = parse_base(state, end)
            continue

        # if there's an index (register, reference, or scaled)
        if indx is None and end.code in (Tokens.DIGIT, Tokens.IDENT, Tokens.AT):
            end, indx = parse_index(state, end)
            continue

        if displacement is None and end.code == Tokens.HEX:
            assert operator is not None
            end, displacement = parse_displacement(state, end, operator)
            continue

        # if there's a minus, we expect an immediate offset
        if end.code == Tokens.MINUS:
            operator = end
            end = state.expect(Tokens.HEX)
            continue

        # if plus we expect an index or a displacement
        if end.code == Tokens.PLUS:
            operator = end
            end = state.expect(Tokens.HEX, Tokens.IDENT, Tokens.AT, Tokens.DIGIT)
            continue

        assert False

    return tree.snippet.Address(
        ref=state.between(start, end),
        size=size and state.extract(size),
        base=base,
        indx=indx,
        disp=displacement,
    )


def parse_base(
    state: ParsingState, token: LexingToken
) -> tuple[LexingToken, tree.snippet.Register | tree.snippet.Reference]:
    if token.code == Tokens.AT:
        base = parse_reference(state, token)

    else:
        base = tree.snippet.Register(
            ref=state.between(token, token),
            name=state.extract(token),
        )

    # base index can be followed by a scaled index or an offset
    token = state.expect(
        Tokens.SQUARE_CLOSE,
        Tokens.PLUS,
        Tokens.MINUS,
        Tokens.IDENT,
        Tokens.AT,
        Tokens.DIGIT,
    )

    return token, base


def parse_index(
    state: ParsingState, token: LexingToken
) -> tuple[LexingToken, tree.snippet.Index]:
    scale: int = 1

    # index can have a scale
    if token.code == Tokens.DIGIT:
        scale = int(state.extract(token))
        _ = state.expect(Tokens.STAR)
        token = state.expect(Tokens.IDENT)

    # index can be a reference
    if token.code == Tokens.AT:
        target = parse_reference(state, token)

    # or just plain register
    else:
        target = tree.snippet.Register(
            ref=state.between(token, token),
            name=state.extract(token),
        )

    indx = tree.snippet.Index(
        ref=state.between(token, token),
        target=target,
        scale=scale,
    )

    token = state.expect(
        Tokens.SQUARE_CLOSE,
        Tokens.PLUS,
        Tokens.MINUS,
    )

    return token, indx


def parse_displacement(
    state: ParsingState, token: LexingToken, operator: LexingToken
) -> tuple[LexingToken, tree.snippet.Displacement]:
    # determine the sign of the displacement
    kind = "forward" if operator.code == Tokens.PLUS else "backward"

    # to be converted to a displacement entry
    displacement = tree.snippet.Displacement(
        ref=state.between(token, token),
        kind=kind,
        offset=extract_hex(state, token),
    )

    # address has to be closed with a square close bracket
    token = state.expect(Tokens.SQUARE_CLOSE)

    return token, displacement


def parse_reference(state: ParsingState, start: LexingToken) -> tree.snippet.Reference:
    # now we expect an identifier
    token = state.expect(Tokens.IDENT)

    # which has to be extracted
    return tree.snippet.Reference(
        ref=state.between(start, token),
        name=state.extract(token),
    )


def parse_label_operand(state: ParsingState, start: LexingToken) -> tree.snippet.Label:
    # the label name is an identifier
    token = state.expect(Tokens.IDENT)

    return tree.snippet.Label(
        ref=state.between(start, token),
        name=state.extract(token),
    )
