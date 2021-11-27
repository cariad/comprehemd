from dataclasses import dataclass, field
from io import StringIO
from typing import IO, List

from comprehemd.blocks import HeadingBlock


@dataclass
class OutlineItem:
    block: HeadingBlock
    children: List["OutlineItem"] = field(default_factory=list)


class Outline:
    def __init__(self) -> None:
        self._root: List[OutlineItem] = []

    def __repr__(self) -> str:
        wip = f"{self.__class__.__name__}("

        if self._root:
            wip += "\n"
            for item in self._root:
                wip += self.make_repr(1, item)

        return wip + ")"

    def __str__(self) -> str:
        writer = StringIO()
        self.render(writer)
        return writer.getvalue()

    def _add(self, item: OutlineItem, to: List[OutlineItem]) -> None:
        if not to:
            # This is the first:
            to.append(item)
            return

        if item.block.level == to[0].block.level:
            # This is a sibling:
            to.append(item)
            return

        if item.block.level < to[0].block.level:
            raise ValueError("Block level is too early")

        # This is a child of the latest item:
        self._add(item=item, to=to[-1].children)

    def _render(
        self,
        indent: int,
        items: List[OutlineItem],
        remaining_levels: int,
        start_level: int,
        writer: IO[str],
    ) -> None:

        indent_str = "  " * indent
        for item in items:

            if items[0].block.level >= start_level and remaining_levels > 0:
                writer.write(
                    f"{indent_str}- [{item.block.text}](#{item.block.anchor})\n"
                )

            self._render(
                indent=indent if items[0].block.level < start_level else indent + 1,
                items=item.children,
                start_level=start_level,
                remaining_levels=remaining_levels
                if items[0].block.level < start_level
                else remaining_levels - 1,
                writer=writer,
            )

    def add(self, block: HeadingBlock) -> None:
        self._add(item=OutlineItem(block), to=self._root)

    @staticmethod
    def make_repr(indent: int, item: OutlineItem) -> str:
        """
        Makes a `repr()` string.

        Arguments:
            indent: Indent.
            item:   Outline item to represent.
        """

        indent_str = "  " * indent
        wip = f"{indent_str}{repr(item.block)}\n"
        for child in item.children:
            wip += Outline.make_repr(indent + 1, child)
        return wip

    def render(self, writer: IO[str], start: int = 1, levels: int = 6) -> None:
        """
        Renders the outline to Markdown.

        Arguments:
            writer: Writer.
            start:  Highest level to render.
            levels: Number of levels beneath `start_level` to render.
        """

        self._render(
            indent=0,
            items=self._root,
            writer=writer,
            start_level=start,
            remaining_levels=levels,
        )

    @property
    def root(self) -> List[OutlineItem]:
        """
        Gets the root outline items.
        """

        return self._root
