from io import StringIO

from comprehemd.blocks import HeadingBlock
from comprehemd.outline import OutlineItem
from comprehemd.read_outline import read_outline


def test_read_outline() -> None:
    reader = StringIO("# one\n\nfoo\n\n## two\n\nbar")
    outline = read_outline(reader)
    assert outline.root == [
        OutlineItem(
            block=HeadingBlock("one", level=1, source="# one"),
            children=[
                OutlineItem(
                    block=HeadingBlock(
                        "two",
                        level=2,
                        source="## two",
                    )
                ),
            ],
        ),
    ]
