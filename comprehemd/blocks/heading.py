from typing import Optional

from comprehemd.blocks.block import Block


class HeadingBlock(Block):
    def __init__(self, text: str, level: int, source: Optional[str] = None) -> None:
        super().__init__(source=source, text=text)
        self._level = level

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}("{self.escaped_text}", level="{self.level}", source="{self.escaped_source}")'

    def __str__(self) -> str:
        return f"{self.__class__.__name__} ({self.level}): {self.escaped_text}"

    @property
    def anchor(self) -> str:
        """
        Gets the anchor.
        """

        return self.make_anchor(self.text)

    @property
    def level(self) -> int:
        """
        Gets the heading level, where 1 is topmost and 6 is bottommost.
        """

        return self._level

    @staticmethod
    def make_anchor(value: str) -> str:
        """
        Makes a GitHub-compatible anchor for `value`.

        Arguments:
            value: Heading to anchor.

        Returns:
            Anchor.
        """

        wip = ""
        for c in value:
            if str.isalnum(c):
                wip += c.lower()
            elif c in [" ", "-"]:
                wip += "-"
        return wip
