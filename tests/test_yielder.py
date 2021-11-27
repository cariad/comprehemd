from io import StringIO
from logging import basicConfig, getLogger
from typing import List

from pytest import mark

from comprehemd import Block, CodeBlock, EmptyBlock, HeadingBlock
from comprehemd.yielder import YieldingMarkdownParser

basicConfig(level="DEBUG")
getLogger("comprehemd").setLevel("DEBUG")


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
        # Heading 1 with pre text and no space
        (
            "pringles\n# foo",
            [
                Block("pringles"),
                HeadingBlock("foo", level=1, source="# foo"),
            ],
        ),
        # Heading 1 with pre text and space
        (
            "pringles\n\n# foo",
            [
                Block("pringles"),
                EmptyBlock(),
                HeadingBlock("foo", level=1, source="# foo"),
            ],
        ),
        # Heading 1 with post text and no space
        (
            "# foo\npringles",
            [
                HeadingBlock("foo", level=1, source="# foo"),
                Block("pringles"),
            ],
        ),
        # Heading 1 with post text and space
        (
            "# foo\n\npringles",
            [
                HeadingBlock("foo", level=1, source="# foo"),
                EmptyBlock(),
                Block("pringles"),
            ],
        ),
    ],
)
def test_heading(feed: str, expect: List[Block]) -> None:
    reader = StringIO(feed)
    parser = YieldingMarkdownParser()
    iterable = parser.read(reader)
    assert list(iterable) == expect


@mark.parametrize(
    "feed, expect",
    [
        # One line
        (
            "    foo: bar",
            [CodeBlock("foo: bar", language=None, source="    foo: bar")],
        ),
        # Two lines
        (
            "    foo: bar\n    woo: war",
            [
                CodeBlock(
                    "foo: bar\nwoo: war",
                    language=None,
                    source="    foo: bar\n    woo: war",
                )
            ],
        ),
        # Three lines
        (
            "    foo: bar\n    woo: war\n    goo: gar",
            [
                CodeBlock(
                    "foo: bar\nwoo: war\ngoo: gar",
                    language=None,
                    source="    foo: bar\n    woo: war\n    goo: gar",
                )
            ],
        ),
        # Two lines with one gap
        (
            "    foo: bar\n\n    woo: war",
            [
                CodeBlock(
                    "foo: bar\n\nwoo: war",
                    language=None,
                    source="    foo: bar\n\n    woo: war",
                )
            ],
        ),
        # Two lines with two gaps
        (
            "    foo: bar\n\n\n    woo: war",
            [
                CodeBlock(
                    "foo: bar\n\n\nwoo: war",
                    language=None,
                    source="    foo: bar\n\n\n    woo: war",
                )
            ],
        ),
        # One line with pre text but no space
        (
            "pringles\n    foo: bar",
            [
                Block("pringles"),
                Block("    foo: bar"),
            ],
        ),
        # One line with pre text and space
        (
            "pringles\n\n    foo: bar",
            [
                Block("pringles"),
                EmptyBlock(),
                CodeBlock("foo: bar", language=None, source="    foo: bar"),
            ],
        ),
        # One line with post text and no space
        (
            "    foo: bar\npringles",
            [
                CodeBlock("foo: bar", language=None, source="    foo: bar"),
                Block("pringles"),
            ],
        ),
        # One line with post text and space
        (
            "    foo: bar\n\npringles",
            [
                CodeBlock("foo: bar", language=None, source="    foo: bar"),
                EmptyBlock(),
                Block("pringles"),
            ],
        ),
        # One line with post text and two spaces
        (
            "    foo: bar\n\n\npringles",
            [
                CodeBlock("foo: bar", language=None, source="    foo: bar"),
                EmptyBlock(),
                EmptyBlock(),
                Block("pringles"),
            ],
        ),
    ],
)
def test_indented_code_block(feed: str, expect: List[Block]) -> None:
    reader = StringIO(feed)
    parser = YieldingMarkdownParser()
    iterable = parser.read(reader)
    assert list(iterable) == expect


@mark.parametrize(
    "feed, expect",
    [
        # One line
        (
            "```yaml\nfoo: bar\n```",
            [CodeBlock("foo: bar", language="yaml", source="```yaml\nfoo: bar\n```")],
        ),
        # Two lines
        (
            "```yaml\nfoo: bar\nwoo: war\n```",
            [
                CodeBlock(
                    "foo: bar\nwoo: war",
                    language="yaml",
                    source="```yaml\nfoo: bar\nwoo: war\n```",
                )
            ],
        ),
        # Three lines
        (
            "```yaml\nfoo: bar\nwoo: war\nmoo: mar\n```",
            [
                CodeBlock(
                    "foo: bar\nwoo: war\nmoo: mar",
                    language="yaml",
                    source="```yaml\nfoo: bar\nwoo: war\nmoo: mar\n```",
                )
            ],
        ),
        # One line with pre text and no space
        (
            "pringles\n```yaml\nfoo: bar\n```",
            [
                Block("pringles"),
                CodeBlock("foo: bar", language="yaml", source="```yaml\nfoo: bar\n```"),
            ],
        ),
        # One line with pre text and space
        (
            "pringles\n\n```yaml\nfoo: bar\n```",
            [
                Block("pringles"),
                EmptyBlock(),
                CodeBlock("foo: bar", language="yaml", source="```yaml\nfoo: bar\n```"),
            ],
        ),
        # One line with post text and no space
        (
            "```yaml\nfoo: bar\n```\npringles",
            [
                CodeBlock("foo: bar", language="yaml", source="```yaml\nfoo: bar\n```"),
                Block("pringles"),
            ],
        ),
        # One line with pre text and space
        (
            "```yaml\nfoo: bar\n```\n\npringles",
            [
                CodeBlock("foo: bar", language="yaml", source="```yaml\nfoo: bar\n```"),
                EmptyBlock(),
                Block("pringles"),
            ],
        ),
    ],
)
def test_fenced_code_block(feed: str, expect: List[Block]) -> None:
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


def test_close_when_already_complete() -> None:
    # This reader ends with \n so close() shouldn't need to do anything.
    reader = StringIO("foo\n")
    y = YieldingMarkdownParser()
    assert list(y.read(reader)) == [Block("foo")]


# def test_outline() -> None:
#     getLogger("comprehemd").debug("lkjlkjlkjlkjlkkljkl")
#     parser = YieldingMarkdownParser(outline=True)
#     parser.feed("# Title\n## Heading\n")
#     parser.close()
#     assert len(parser.outline.root) == 1
#     assert parser.outline.root[0].block.text == "Title"
#     assert len(parser.outline.root[0].children) == 1
#     assert parser.outline.root[0].children[0].block.text == "Heading"


# def test_outline__none() -> None:
#     parser = MarkdownParser()
#     with raises(ValueError):
#         parser.outline
