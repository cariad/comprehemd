from io import StringIO

from pytest import mark, raises

from comprehemd.blocks import HeadingBlock
from comprehemd.outline import Outline, OutlineItem


def test_add__first() -> None:
    outline = Outline()
    outline.add(HeadingBlock("one", level=1, source=""))
    assert outline.root == [
        OutlineItem(block=HeadingBlock("one", level=1, source="")),
    ]


def test_add__first_sibling() -> None:
    outline = Outline()
    outline.add(HeadingBlock("one a", level=1, source=""))
    outline.add(HeadingBlock("one b", level=1, source=""))
    assert outline.root == [
        OutlineItem(block=HeadingBlock("one a", level=1, source="")),
        OutlineItem(block=HeadingBlock("one b", level=1, source="")),
    ]


def test_add__first_child() -> None:
    outline = Outline()
    outline.add(HeadingBlock("one", level=1, source=""))
    outline.add(HeadingBlock("two", level=2, source=""))
    assert outline.root == [
        OutlineItem(
            block=HeadingBlock("one", level=1, source=""),
            children=[
                OutlineItem(block=HeadingBlock("two", level=2, source="")),
            ],
        ),
    ]


def test_add__first_sibling_child() -> None:
    outline = Outline()
    outline.add(HeadingBlock("one a", level=1, source=""))
    outline.add(HeadingBlock("one b", level=1, source=""))
    outline.add(HeadingBlock("two", level=2, source=""))
    assert outline.root == [
        OutlineItem(block=HeadingBlock("one a", level=1, source="")),
        OutlineItem(
            block=HeadingBlock("one b", level=1, source=""),
            children=[
                OutlineItem(block=HeadingBlock("two", level=2, source="")),
            ],
        ),
    ]


def test_add__first_too_early() -> None:
    outline = Outline()
    outline.add(HeadingBlock("two", level=2, source=""))
    with raises(ValueError):
        outline.add(HeadingBlock("one", level=1, source=""))


def test_add__second_too_early() -> None:
    outline = Outline()
    outline.add(HeadingBlock("one", level=1, source=""))
    outline.add(HeadingBlock("three", level=3, source=""))
    with raises(ValueError):
        outline.add(HeadingBlock("two", level=2, source=""))


def test_render__empty() -> None:
    writer = StringIO()
    outline = Outline()
    outline.render(writer)
    assert writer.getvalue() == ""


def test_render__first() -> None:
    outline = Outline()
    outline.add(HeadingBlock("one", level=1, source=""))
    writer = StringIO()
    outline.render(writer)
    assert (
        writer.getvalue()
        == """- [one](#one)
"""
    )


def test_render__first_sibling() -> None:
    outline = Outline()
    outline.add(HeadingBlock("one a", level=1, source=""))
    outline.add(HeadingBlock("one b", level=1, source=""))
    writer = StringIO()
    outline.render(writer)
    assert (
        writer.getvalue()
        == """- [one a](#one-a)
- [one b](#one-b)
"""
    )


def test_render__first_child() -> None:
    outline = Outline()
    outline.add(HeadingBlock("one", level=1, source=""))
    outline.add(HeadingBlock("two", level=2, source=""))
    writer = StringIO()
    outline.render(writer)
    assert (
        writer.getvalue()
        == """- [one](#one)
  - [two](#two)
"""
    )


def test_render__first_sibling_child() -> None:
    outline = Outline()
    outline.add(HeadingBlock("one a", level=1, source=""))
    outline.add(HeadingBlock("one b", level=1, source=""))
    outline.add(HeadingBlock("two", level=2, source=""))
    writer = StringIO()
    outline.render(writer)
    assert (
        writer.getvalue()
        == """- [one a](#one-a)
- [one b](#one-b)
  - [two](#two)
"""
    )


@mark.parametrize(
    "start, levels, expect",
    [
        (1, 1, "- [one a](#one-a)\n- [one b](#one-b)\n"),
        (
            1,
            2,
            "- [one a](#one-a)\n- [one b](#one-b)\n  - [two a](#two-a)\n  - [two b](#two-b)\n",
        ),
        (
            2,
            3,
            "- [two a](#two-a)\n- [two b](#two-b)\n  - [three a](#three-a)\n  - [three b](#three-b)\n    - [four a](#four-a)\n    - [four b](#four-b)\n",
        ),
    ],
)
def test_render__range(start: int, levels: int, expect: str) -> None:
    outline = Outline()
    outline.add(HeadingBlock("one a", level=1, source=""))
    outline.add(HeadingBlock("one b", level=1, source=""))
    outline.add(HeadingBlock("two a", level=2, source=""))
    outline.add(HeadingBlock("two b", level=2, source=""))
    outline.add(HeadingBlock("three a", level=3, source=""))
    outline.add(HeadingBlock("three b", level=3, source=""))
    outline.add(HeadingBlock("four a", level=4, source=""))
    outline.add(HeadingBlock("four b", level=4, source=""))
    outline.add(HeadingBlock("five a", level=5, source=""))
    outline.add(HeadingBlock("five b", level=5, source=""))
    outline.add(HeadingBlock("six a", level=6, source=""))
    outline.add(HeadingBlock("six b", level=6, source=""))
    writer = StringIO()
    outline.render(writer, start_level=start, levels=levels)
    assert writer.getvalue() == expect
