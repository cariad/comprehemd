from io import StringIO
from logging import basicConfig, getLogger
from typing import List

from pytest import mark

from comprehemd import Block, CodeBlock, HeadingBlock
from comprehemd.yielder import YieldingMarkdownParser

basicConfig(level="DEBUG")
getLogger("comprehemd").setLevel("DEBUG")


def test_read__block() -> None:
    reader = StringIO("foo")
    y = YieldingMarkdownParser()
    actual = list(y.read(reader))

    assert actual == [
        Block("foo", source="foo"),
    ]


@mark.parametrize(
    "feed, expect",
    [
        # Heading 1
        ("# foo", [HeadingBlock("foo", level=1, source="# foo")]),
        # Heading 2
        ("## foo", [HeadingBlock("foo", level=2, source="## foo")]),
        # Heading 3
        ("### foo", [HeadingBlock("foo", level=3, source="### foo")]),
        # Heading 4
        ("#### foo", [HeadingBlock("foo", level=4, source="#### foo")]),
        # Heading 5
        ("##### foo", [HeadingBlock("foo", level=5, source="##### foo")]),
        # Heading 6
        ("###### foo", [HeadingBlock("foo", level=6, source="###### foo")]),
        # One line of backtick fenced code
        (
            "```json\n{}\n```",
            [CodeBlock("{}", language="json", source="```json\n{}\n```")],
        ),
    ],
)
def test(feed: str, expect: List[Block]) -> None:
    reader = StringIO(feed)
    parser = YieldingMarkdownParser()
    iterable = parser.read(reader)
    assert list(iterable) == expect


def test_incomplete_fenced_code() -> None:
    reader = StringIO("```json\n{")
    y = YieldingMarkdownParser()
    actual = list(y.read(reader))

    assert actual == [
        Block("```json"),
        Block("{"),
    ]
