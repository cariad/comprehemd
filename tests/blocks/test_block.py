from typing import Any

from pytest import mark

from comprehemd.blocks import Block, HeadingBlock


@mark.parametrize(
    "a, b, expect",
    [
        (Block("foo"), HeadingBlock("foo", level=1), False),
        (Block("foo"), Block("foo\n"), False),
        (Block("foo", source="foo"), Block("foo", source="foo\n"), False),
        (Block("foo"), Block("foo"), True),
    ],
)
def test_eq(a: Block, b: Any, expect: bool) -> None:
    assert (a == b) is expect


def test_repr() -> None:
    block = Block("foo\nbar", source="foo\nbar\n")
    assert repr(block) == 'Block("foo\\nbar", source="foo\\nbar\\n")'


def test_str() -> None:
    block = Block("foo\nbar", source="foo\nbar\n")
    assert str(block) == "Block: foo\\nbar"


@mark.parametrize(
    "block, expect",
    [
        (Block("foo"), 0),
        (Block("foo\n"), 1),
        (Block("foo\n\n"), 2),
        (Block("\n\n\n"), 3),
        (Block(""), 0),
    ],
)
def test_trailing_new_lines(block: Block, expect: int) -> None:
    assert block.trailing_new_lines == expect
