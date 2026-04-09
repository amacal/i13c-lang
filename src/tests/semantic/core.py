from pytest import raises

from i13c.semantic.core import default_range, default_width


def can_reject_unknown_type_for_default_width():
    with raises(ValueError, match="Unknown type name: i128"):
        default_width(b"i128")


def can_reject_unknown_type_for_default_range():
    with raises(ValueError, match="Unknown type name: i128"):
        default_range(b"i128")
