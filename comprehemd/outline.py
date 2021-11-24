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
        if not self._root:
            return f"{self.__class__.__name__}: empty"

        wip = ""

        for item in self._root:
            wip += repr(item) + "\n"

        return wip

    def __str__(self) -> str:
        writer = StringIO()
        self.render(writer)
        return writer.getvalue()

    def add(self, block: HeadingBlock) -> None:
        self._add(item=OutlineItem(block), to=self._root)

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

    def render(self, writer: IO[str], start_level: int = 1, levels: int = 6) -> None:
        self._render(
            indent=0,
            items=self._root,
            writer=writer,
            start_level=start_level,
            remaining_levels=levels,
        )

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

    @property
    def root(self) -> List[OutlineItem]:
        return self._root
