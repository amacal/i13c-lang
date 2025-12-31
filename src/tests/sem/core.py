from i13c.sem import core


def can_derive_width_respects_boundaries():
    # 0 fits in 8 bits (zero-width edge, still 8-bit bucket).
    assert core.derive_width(0) == 8

    # 0xff is the max 8-bit value.
    assert core.derive_width(0xFF) == 8

    # 0x100 is the first value that needs 9 bits, so 16-bit bucket.
    assert core.derive_width(0x100) == 16

    # 0xffff is the max 16-bit value.
    assert core.derive_width(0xFFFF) == 16

    # 0x1_0000 is the first value that needs 17 bits, so 32-bit bucket.
    assert core.derive_width(0x1_0000) == 32

    # 0xffff_ffff is the max 32-bit value.
    assert core.derive_width(0xFFFF_FFFF) == 32

    # 0x1_0000_0000 is the first value that needs 33 bits, so 64-bit bucket.
    assert core.derive_width(0x1_0000_0000) == 64

    # 0xffff_ffff_ffff_ffff is the max 64-bit value.
    assert core.derive_width(0xFFFF_FFFF_FFFF_FFFF) == 64
