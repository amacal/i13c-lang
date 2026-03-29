# fmt: off
ELFCLASS64 = 0x02     # 64-bit objects
ELFDATA2LSB = 0x01    # little-endian
EV_CURRENT = 0x01     # current version
ELFOSABI_SYSV = 0x00  # System V ABI
ET_EXEC = 0x02        # executable file
EM_X86_64 = 0x3E      # AMD x86-64 architecture

TEXT_ALIGN = 0x0001  # no alignment
PT_LOAD = 0x01       # loadable program segment
PF_X = 0x1           # execute
PF_R = 0x4           # read

ELF_HEADER_SIZE = 64
PROGRAM_HEADER_SIZE = 56
ELF_BASE_ADDR = 0x400000
ENTRY_POINT = ELF_BASE_ADDR + ELF_HEADER_SIZE + PROGRAM_HEADER_SIZE
# fmt: on


def as_bytes(value: int, length: int) -> bytes:
    return value.to_bytes(length, byteorder="little")


def emit(code: bytes) -> bytes:
    content = bytearray()
    code_size = len(code)

    # layout: [ehdr][phdr][code]
    file_off_code = ELF_HEADER_SIZE + PROGRAM_HEADER_SIZE
    entry_point = ELF_BASE_ADDR + file_off_code
    file_size = file_off_code + code_size

    emit_ehdr(content, entry_point)
    emit_phdr(content, file_size)
    content.extend(code)

    return bytes(content)


def emit_ehdr(content: bytearray, entry_point: int) -> None:

    # fmt: off
    eident = bytes(
        [0x7F, 0x45, 0x4C, 0x46,
        ELFCLASS64, ELFDATA2LSB, EV_CURRENT, ELFOSABI_SYSV,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    )

    content.extend(eident)                           # e_ident[16]
    content.extend(as_bytes(ET_EXEC, 2))             # e_type
    content.extend(as_bytes(EM_X86_64, 2))           # e_machine
    content.extend(as_bytes(EV_CURRENT, 4))          # e_version
    content.extend(as_bytes(entry_point, 8))         # e_entry
    content.extend(as_bytes(ELF_HEADER_SIZE, 8))     # e_phoff (phdr right after ehdr)
    content.extend(as_bytes(0, 8))                   # e_shoff (no sections)
    content.extend(as_bytes(0, 4))                   # e_flags
    content.extend(as_bytes(ELF_HEADER_SIZE, 2))     # e_ehsize
    content.extend(as_bytes(PROGRAM_HEADER_SIZE, 2)) # e_phentsize
    content.extend(as_bytes(1, 2))                   # e_phnum
    content.extend(as_bytes(0, 2))                   # e_shentsize
    content.extend(as_bytes(0, 2))                   # e_shnum
    content.extend(as_bytes(0, 2))                   # e_shstrndx
    # fmt: on


def emit_phdr(content: bytearray, file_size: int) -> None:
    # fmt: off
    content.extend(as_bytes(PT_LOAD, 4))             # p_type
    content.extend(as_bytes(PF_R | PF_X, 4))         # p_flags
    content.extend(as_bytes(0, 8))                   # p_offset (from file start)
    content.extend(as_bytes(ELF_BASE_ADDR, 8))       # p_vaddr
    content.extend(as_bytes(ELF_BASE_ADDR, 8))       # p_paddr
    content.extend(as_bytes(file_size, 8))           # p_filesz (map whole file)
    content.extend(as_bytes(file_size, 8))           # p_memsz  (no bss)
    content.extend(as_bytes(TEXT_ALIGN, 8))          # p_align  (1 for simplest)
    # fmt: on
