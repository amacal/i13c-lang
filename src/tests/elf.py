from i13c import elf


def can_emit_elf():
    code = bytes([0x90, 0x90, 0x90])
    elf_binary = elf.emit(code)

    assert elf_binary[0:4] == b"\x7fELF"
    assert elf_binary[4] == elf.ELFCLASS64
    assert elf_binary[5] == elf.ELFDATA2LSB
    assert int.from_bytes(elf_binary[24:32], "little") == elf.ENTRY_POINT

    code_offset = elf.ELF_HEADER_SIZE + elf.PROGRAM_HEADER_SIZE
    assert elf_binary[code_offset : code_offset + len(code)] == code
