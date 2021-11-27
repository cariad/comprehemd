from pytest import mark

from comprehemd.blocks import HeadingBlock


def test_repr() -> None:
    block = HeadingBlock("foo", level=1, source="foo\n")
    assert repr(block) == 'HeadingBlock("foo", level="1", source="foo\\n")'


def test_str() -> None:
    block = HeadingBlock("foo", level=1, source="foo\n")
    assert str(block) == "HeadingBlock (1): foo"


@mark.parametrize(
    "value, expect",
    [
        ("foo", "foo"),
        ("🍕 Pizza", "-pizza"),
        ("gem _and_ gemmy", "gem-and-gemmy"),
    ],
)
def test_anchor(value: str, expect: str) -> None:
    assert HeadingBlock.make_anchor(value) == expect
