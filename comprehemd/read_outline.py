from typing import IO

from comprehemd.blocks import HeadingBlock
from comprehemd.outline import Outline
from comprehemd.yielder import YieldingMarkdownParser


def read_outline(reader: IO[str]) -> Outline:
    outline = Outline()
    parser = YieldingMarkdownParser()
    for block in parser.read(reader):
        if isinstance(block, HeadingBlock):
            outline.add(block)
    return outline
