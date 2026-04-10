from typing import List, Optional, Tuple

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
    instructions: List[tree.snippet.Instruction] = []
    slots: List[tree.snippet.Slot] = []
    clobbers: List[tree.snippet.Register] = []
    noreturn: bool = False

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
        clobbers, noreturn = parse_snippet_flags(state)

    # expect opening curly brace
    state.expect(Tokens.CURLY_OPEN)

    # parse instructions until closing curly brace
    while not state.is_in(Tokens.CURLY_CLOSE):
        instructions.append(parse_instruction(state))

    # expect closed curly brace
    state.expect(Tokens.CURLY_CLOSE)

    return tree.snippet.Snippet(
        ref=state.between(name, end),
        name=state.extract(name),
        noreturn=noreturn,
        clobbers=clobbers,
        slots=slots,
        instructions=instructions,
    )


def parse_slots(state: ParsingState) -> List[tree.snippet.Slot]:
    parameters: List[tree.snippet.Slot] = []
    parameters.append(parse_slot(state))

    # a comma suggests next parameter
    while state.accept(Tokens.COMMA):
        parameters.append(parse_slot(state))

    return parameters


def parse_slot(state: ParsingState) -> tree.snippet.Slot:
    range: Optional[tree.types.Range] = None
    ident = state.expect(Tokens.IDENT)

    # expect '@' followed by register or immediate
    state.expect(Tokens.AT)
    bind = state.expect(Tokens.REG, Tokens.KEYWORD)

    # if it's a keyword, it has to be "imm"
    if bind.code == Tokens.KEYWORD:
        if state.extract(bind) != b"imm":
            raise UnexpectedKeyword(bind, [b"imm"], state.extract(bind))

    # expect ':' followed by type
    state.expect(Tokens.COLON)
    type = state.expect(Tokens.IDENT)

    if state.is_in(Tokens.SQUARE_OPEN):
        range = parse_range(state)

    return tree.snippet.Slot(
        name=state.extract(ident),
        bind=tree.snippet.Bind(
            ref=state.between(bind, bind),
            name=state.extract(bind),
        ),
        type=tree.types.Type(
            ref=state.between(type, type),
            name=state.extract(type),
            range=range,
        ),
    )


def parse_snippet_flags(
    state: ParsingState,
) -> Tuple[List[tree.snippet.Register], bool]:
    keyword: Optional[LexingToken] = None
    clobbers: Optional[List[tree.snippet.Register]] = None
    terminal = False

    while not state.is_in(Tokens.CURLY_OPEN):
        expected = {b"clobbers", b"noreturn"}
        keyword = state.expect(Tokens.KEYWORD)

        # fail if the keyword is not "noreturn"
        if state.extract(keyword) not in expected:
            raise UnexpectedKeyword(keyword, expected, state.extract(keyword))

        # if "clobbers", parse the clobber list
        if state.extract(keyword) == b"clobbers":
            if clobbers is not None:
                raise FlagAlreadySpecified(keyword, b"clobbers")
            else:
                clobbers = parse_clobbers(state)

        # if "noreturn", set terminal flag
        elif state.extract(keyword) == b"noreturn":
            if terminal:
                raise FlagAlreadySpecified(keyword, b"noreturn")
            else:
                terminal = True

    return clobbers or [], terminal


def parse_clobbers(state: ParsingState) -> List[tree.snippet.Register]:
    clobbers: List[tree.snippet.Register] = []

    # at least one register is expected
    clobber = state.expect(Tokens.REG)
    clobbers.append(
        tree.snippet.Register(
            ref=state.span(clobber),
            name=state.extract(clobber),
        )
    )

    # a comma suggests next clobber
    while state.accept(Tokens.COMMA):
        clobber = state.expect(Tokens.REG)
        clobbers.append(
            tree.snippet.Register(
                ref=state.span(clobber),
                name=state.extract(clobber),
            )
        )

    return clobbers


def parse_instruction(state: ParsingState) -> tree.snippet.Instruction:
    operands: List[tree.snippet.Operand] = []
    token = state.expect(Tokens.IDENT)

    # optional operands
    if state.is_in(*OPERANDS_START):
        operands = parse_operands(state)

    # expect a semicolon
    end = state.expect(Tokens.SEMICOLON)

    # build instruction and token reference
    mnemonic = tree.snippet.Mnemonic(name=state.extract(token))

    return tree.snippet.Instruction(
        ref=state.between(token, end),
        mnemonic=mnemonic,
        operands=operands,
    )


OPERANDS_START = [Tokens.REG, Tokens.HEX, Tokens.AT, Tokens.SQUARE_OPEN]


def parse_operands(state: ParsingState) -> List[tree.snippet.Operand]:
    operands: List[tree.snippet.Operand] = []
    operands.append(parse_operand(state))

    # a comma suggests next operand
    while state.accept(Tokens.COMMA):
        operands.append(parse_operand(state))

    return operands


def parse_operand(state: ParsingState) -> tree.snippet.Operand:
    token = state.expect(*OPERANDS_START)

    # register has to provide its name
    if token.code == Tokens.REG:
        return tree.snippet.Register(ref=state.span(token), name=state.extract(token))

    # immediate has to provide its decimal value
    elif token.code == Tokens.HEX:
        return tree.snippet.Immediate(
            ref=state.span(token),
            value=extract_hex(state, token),
        )

    # reference has to provide its identifier
    elif token.code == Tokens.AT:
        # now we expect an identifier
        token = state.expect(Tokens.IDENT)

        # which has to be extracted
        return tree.snippet.Reference(
            ref=state.span(token),
            name=state.extract(token),
        )

    # address operands starts with a square open bracket
    else:
        offset: Optional[tree.snippet.Offset] = None

        # now we expect a register as the base
        base = state.expect(Tokens.REG)

        # optionally, an offset can be provided
        end = state.expect(Tokens.SQUARE_CLOSE, Tokens.PLUS, Tokens.MINUS)

        if end.code == Tokens.PLUS or end.code == Tokens.MINUS:
            # if there's a plus or minus, we expect an immediate offset
            value = state.expect(Tokens.HEX)

            # determine the sign of the offset
            kind = "forward" if end.code == Tokens.PLUS else "backward"

            # to be converted to an offset operand
            offset = tree.snippet.Offset(
                kind=kind,
                value=extract_hex(state, value),
            )

            # address has to be closed with a square close bracket
            end = state.expect(Tokens.SQUARE_CLOSE)

        return tree.snippet.Address(
            ref=state.between(token, end),
            base=tree.snippet.Register(ref=state.span(base), name=state.extract(base)),
            offset=offset,
        )
