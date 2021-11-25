from logging import basicConfig, getLogger
from typing import Any, List

from pytest import mark

from comprehemd import MarkdownParser
from comprehemd.blocks import Block, CodeBlock, HeadingBlock

basicConfig(level="DEBUG")
getLogger("comprehemd").setLevel("DEBUG")


class FooParser(MarkdownParser):
    def __init__(self) -> None:
        super().__init__()
        self.log: List[Any] = []

    def handle_block(self, block: Block) -> None:
        self.log.append(block)


@mark.parametrize(
    "feeds, expect",
    [
        (
            ["#", " ", "f", "o", "o", "\n"],
            [HeadingBlock("foo", level=1, source="# foo\n")],
        ),
        (["# one\n"], [HeadingBlock("one", level=1, source="# one\n")]),
        (["## two\n"], [HeadingBlock("two", level=2, source="## two\n")]),
        (["### three\n"], [HeadingBlock("three", level=3, source="### three\n")]),
        (["#### four\n"], [HeadingBlock("four", level=4, source="#### four\n")]),
        (["##### five\n"], [HeadingBlock("five", level=5, source="##### five\n")]),
        (["###### six\n"], [HeadingBlock("six", level=6, source="###### six\n")]),
        # Paragraphs:
        (["Hello, world!\n"], [Block("Hello, world!", source="Hello, world!\n")]),
        # Fenced code blocks:
        (
            [
                "```yaml\n",
                "foo: bar\n",
                "```",
            ],
            [
                CodeBlock(
                    "foo: bar",
                    language="yaml",
                    source="```yaml\nfoo: bar\n```\n",
                )
            ],
        ),
        (
            [
                "~~~yaml\n",
                "foo: bar\n",
                "~~~",
            ],
            [
                CodeBlock(
                    "foo: bar",
                    language="yaml",
                    source="~~~yaml\nfoo: bar\n~~~\n",
                )
            ],
        ),
        (
            [
                "```yaml\n",
                "foo: bar\n",
                "woo: boo\n",
                "```",
            ],
            [
                CodeBlock(
                    "foo: bar\nwoo: boo",
                    language="yaml",
                    source="```yaml\nfoo: bar\nwoo: boo\n```\n",
                )
            ],
        ),
        (
            [
                "~~~yaml\n",
                "foo: bar\n",
                "woo: boo\n",
                "~~~",
            ],
            [
                CodeBlock(
                    "foo: bar\nwoo: boo",
                    language="yaml",
                    source="~~~yaml\nfoo: bar\nwoo: boo\n~~~\n",
                )
            ],
        ),
        # Incomplete fenced block:
        (
            [
                "```yaml\n",
                "foo: bar",
            ],
            [
                Block("```yaml", source="```yaml\n"),
                Block("foo: bar", source="foo: bar\n"),
            ],
        ),
        # Indented code blocks:
        (
            [
                "    foo: bar\n",
            ],
            [CodeBlock("foo: bar", source="    foo: bar\n")],
        ),
        (
            [
                "No empty line:\n",
                "    foo: bar\n",
            ],
            [
                Block(
                    "No empty line:",
                    source="No empty line:\n",
                ),
                Block("    foo: bar", source="    foo: bar\n"),
            ],
        ),
        (
            [
                "    foo: bar\n",
                "\n",
                "Subsequent text.\n",
            ],
            [
                CodeBlock("foo: bar", source="    foo: bar\n"),
                Block("", source="\n"),
                Block("Subsequent text.", source="Subsequent text.\n"),
            ],
        ),
        (
            [
                "    foo: bar\n",
                "\n",
                "\n",
                "Subsequent text.",
            ],
            [
                CodeBlock("foo: bar", source="    foo: bar\n"),
                Block("", source="\n"),
                Block("", source="\n"),
                Block("Subsequent text.", source="Subsequent text.\n"),
            ],
        ),
    ],
)
def test(feeds: List[str], expect: List[str]) -> None:
    parser = FooParser()
    for feed in feeds:
        parser.feed(feed)
    parser.close()
    assert parser.log == expect
