from io import StringIO

from pytest import mark

from comprehemd import Fence
from comprehemd.blocks import CodeBlock


@mark.parametrize(
    "block, expect",
    [
        (
            CodeBlock("foo", source="foo\n"),
            'CodeBlock("foo", language="<None>", source="foo\\n")',
        ),
        (
            CodeBlock("foo", language="bar", source="foo\n"),
            'CodeBlock("foo", language="bar", source="foo\\n")',
        ),
    ],
)
def test_repr(block: CodeBlock, expect: str) -> None:
    assert repr(block) == expect


@mark.parametrize(
    "block, expect",
    [
        (
            CodeBlock("foo", source="foo\n"),
            "CodeBlock (<None>): foo",
        ),
        (
            CodeBlock("foo", language="bar", source="foo\n"),
            "CodeBlock (bar): foo",
        ),
    ],
)
def test_str(block: CodeBlock, expect: str) -> None:
    assert str(block) == expect


@mark.parametrize(
    "block, fence, expect",
    [
        (
            CodeBlock("foo"),
            Fence.BACKTICKS,
            "```\nfoo\n```\n",
        ),
        (
            CodeBlock("foo", language="bar"),
            Fence.BACKTICKS,
            "```bar\nfoo\n```\n",
        ),
        (
            CodeBlock("foo\n", language="bar"),
            Fence.BACKTICKS,
            "```bar\nfoo\n```\n",
        ),
        (
            CodeBlock("foo", language="bar"),
            Fence.TILDES,
            "~~~bar\nfoo\n~~~\n",
        ),
    ],
)
def test_render(block: CodeBlock, fence: Fence, expect: str) -> None:
    writer = StringIO()
    block.render(writer, fence=fence)
    assert writer.getvalue() == expect
