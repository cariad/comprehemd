# from logging import basicConfig, getLogger
# from typing import Any, List

# from pytest import mark, raises

# from comprehemd import MarkdownParser
# from comprehemd.blocks import Block, CodeBlock, HeadingBlock

# basicConfig(level="DEBUG")
# getLogger("comprehemd").setLevel("DEBUG")


# class FooParser(MarkdownParser):
#     def __init__(self) -> None:
#         super().__init__()
#         self.log: List[Any] = []

#     def handle_block(self, block: Block) -> None:
#         self.log.append(block)


# @mark.parametrize(
#     "feeds, expect",
#     [
#         (
#             ["#", " ", "f", "o", "o", "\n"],
#             [HeadingBlock("foo", level=1, source="# foo")],
#         ),
#         (["# one\n"], [HeadingBlock("one", level=1, source="# one")]),
#         (["## two\n"], [HeadingBlock("two", level=2, source="## two")]),
#         (["### three\n"], [HeadingBlock("three", level=3, source="### three")]),
#         (["#### four\n"], [HeadingBlock("four", level=4, source="#### four")]),
#         (["##### five\n"], [HeadingBlock("five", level=5, source="##### five")]),
#         (["###### six\n"], [HeadingBlock("six", level=6, source="###### six")]),
#         # Paragraphs:
#         (["Hello, world!\n"], [Block("Hello, world!")]),
#         # Fenced code blocks:
#         (
#             [
#                 "```yaml\n",
#                 "foo: bar\n",
#                 "```",
#             ],
#             [
#                 CodeBlock(
#                     "foo: bar",
#                     language="yaml",
#                     source="```yaml\nfoo: bar\n```",
#                 )
#             ],
#         ),
#         (
#             [
#                 "~~~yaml\n",
#                 "foo: bar\n",
#                 "~~~",
#             ],
#             [
#                 CodeBlock(
#                     "foo: bar",
#                     language="yaml",
#                     source="~~~yaml\nfoo: bar\n~~~",
#                 )
#             ],
#         ),
#         (
#             [
#                 "```yaml\n",
#                 "foo: bar\n",
#                 "woo: boo\n",
#                 "```",
#             ],
#             [
#                 CodeBlock(
#                     "foo: bar\nwoo: boo",
#                     language="yaml",
#                     source="```yaml\nfoo: bar\nwoo: boo\n```",
#                 )
#             ],
#         ),
#         (
#             [
#                 "~~~yaml\n",
#                 "foo: bar\n",
#                 "woo: boo\n",
#                 "~~~",
#             ],
#             [
#                 CodeBlock(
#                     "foo: bar\nwoo: boo",
#                     language="yaml",
#                     source="~~~yaml\nfoo: bar\nwoo: boo\n~~~",
#                 )
#             ],
#         ),
#         # Incomplete fenced block:
#         (
#             [
#                 "```yaml\n",
#                 "foo: bar",
#             ],
#             [
#                 Block("```yaml"),
#                 Block("foo: bar"),
#             ],
#         ),
#         # Indented code blocks:
#         (
#             [
#                 "    foo: bar\n",
#             ],
#             [CodeBlock("foo: bar", source="    foo: bar")],
#         ),
#         (
#             [
#                 "No empty line:\n",
#                 "    foo: bar\n",
#             ],
#             [
#                 Block("No empty line:"),
#                 Block("    foo: bar", source="    foo: bar"),
#             ],
#         ),
#         (
#             [
#                 "    foo: bar\n",
#                 "\n",
#                 "Subsequent text.\n",
#             ],
#             [
#                 CodeBlock("foo: bar", source="    foo: bar"),
#                 Block(""),
#                 Block("Subsequent text."),
#             ],
#         ),
#         (
#             [
#                 "    foo: bar\n",
#                 "\n",
#                 "\n",
#                 "Subsequent text.",
#             ],
#             [
#                 CodeBlock("foo: bar", source="    foo: bar"),
#                 Block(""),
#                 Block(""),
#                 Block("Subsequent text."),
#             ],
#         ),
#     ],
# )
# def test(feeds: List[str], expect: List[str]) -> None:
#     parser = FooParser()
#     for feed in feeds:
#         parser.feed(feed)
#     parser.close()
#     assert parser.log == expect


# def test_outline() -> None:
#     parser = MarkdownParser(outline=True)
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


# # def test_read() -> None:
# #     reader = StringIO("# Title\n## Heading\n")
# #     parser = MarkdownParser()
# #     parser.feed("# Title\n## Heading\n")
# #     parser.close()
# #     assert len(parser.outline.root) == 1
# #     assert parser.outline.root[0].block.text == "Title"
# #     assert len(parser.outline.root[0].children) == 1
# #     assert parser.outline.root[0].children[0].block.text == "Heading"
