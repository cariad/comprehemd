from pytest import mark

from comprehemd.code_patterns import TildesPattern


@mark.parametrize(
    "line, expect",
    [
        ("~~~", True),
        ("~~~~", False),
    ],
)
def test_end_expression(line: str, expect: bool) -> None:
    assert TildesPattern().is_end(line) is expect


def test_fenced() -> None:
    assert TildesPattern().fenced
