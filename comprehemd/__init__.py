import importlib.resources as pkg_resources

from comprehemd.blocks import Block, CodeBlock, EmptyBlock, HeadingBlock
from comprehemd.fence import Fence
from comprehemd.outline import Outline, OutlineItem
from comprehemd.parser import MarkdownParser
from comprehemd.read_outline import read_outline

with pkg_resources.open_text(__package__, "VERSION") as t:
    __version__ = t.readline().strip()

__all__ = [
    "Block",
    "CodeBlock",
    "EmptyBlock",
    "Fence",
    "HeadingBlock",
    "Outline",
    "OutlineItem",
    "read_outline",
    "MarkdownParser",
]
