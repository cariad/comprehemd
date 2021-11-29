import importlib.resources as pkg_resources

from comprehemd.blocks import Block, CodeBlock, EmptyBlock, HeadingBlock
from comprehemd.fence import Fence
from comprehemd.parser import MarkdownParser

with pkg_resources.open_text(__package__, "VERSION") as t:
    __version__ = t.readline().strip()

__all__ = [
    "Block",
    "CodeBlock",
    "EmptyBlock",
    "Fence",
    "HeadingBlock",
    "MarkdownParser",
]
