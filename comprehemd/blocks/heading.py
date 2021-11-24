from typing import Optional

from comprehemd.blocks.block import Block


class HeadingBlock(Block):
    def __init__(self, text: str, level: int, source: Optional[str] = None) -> None:
        super().__init__(source=source, text=text)
        self._level = level

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(level={self.level}, source={self.text}, text={self.text})"

    def __str__(self) -> str:
        return f"{self.__class__.__name__} ({self.level}): {self.text}"

    @property
    def anchor(self) -> str:
        wip = ""
        for c in self.text:
            if str.isalnum(c):
                wip += c.lower()
            elif c in [" ", "-"]:
                wip += "-"
        return wip

    @property
    def level(self) -> int:
        return self._level
