from comprehemd.blocks import EmptyBlock


def test_repr() -> None:
    assert repr(EmptyBlock()) == "EmptyBlock"


def test_str() -> None:
    assert str(EmptyBlock()) == "EmptyBlock"
