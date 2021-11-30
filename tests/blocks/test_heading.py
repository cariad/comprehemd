from comprehemd.blocks import HeadingBlock


def test_repr() -> None:
    block = HeadingBlock("foo", level=1, source="foo\n")
    assert repr(block) == 'HeadingBlock("foo", level="1", source="foo\\n")'


def test_str() -> None:
    block = HeadingBlock("foo", level=1, source="foo\n")
    assert str(block) == "HeadingBlock (1): foo"
