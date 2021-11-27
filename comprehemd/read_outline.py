from typing import IO

from comprehemd.blocks import HeadingBlock
from comprehemd.outline import Outline
from comprehemd.parser import MarkdownParser


def read_outline(reader: IO[str]) -> Outline:
    outline = Outline()
    parser = MarkdownParser()
    for block in parser.read(reader):
        if isinstance(block, HeadingBlock):
            outline.add(block)
    return outline
