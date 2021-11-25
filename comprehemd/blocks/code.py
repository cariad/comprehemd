from typing import IO, Optional

from comprehemd.blocks.block import Block
from comprehemd.fence import Fence


class CodeBlock(Block):
    def __init__(
        self,
        text: str,
        language: Optional[str] = None,
        source: Optional[str] = None,
    ) -> None:
        super().__init__(source=source, text=text)
        self._language = language

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}("{self.escaped_text}", language="{self.loggable_language}", source="{self.escaped_source}")'

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__} ({self.loggable_language}): {self.escaped_text}"
        )

    @property
    def language(self) -> Optional[str]:
        """
        Gets the language.
        """

        return self._language

    @property
    def loggable_language(self) -> str:
        """
        Gets the language forced to a loggable string.
        """

        return self.language or "<None>"

    def render(self, writer: IO[str], fence: Fence = Fence.BACKTICKS) -> None:
        """
        Renders the code block to Markdown.

        Arguments:
            writer: Writer.
            fence:  Fence. Defaults to backticks.
        """

        fence_str = "~~~" if fence == Fence.TILDES else "```"
        writer.write(fence_str)
        if self.language:
            writer.write(self.language)
        writer.write("\n")
        writer.write(self.text)
        if not self.text.endswith("\n"):
            writer.write("\n")
        writer.write(fence_str)
        writer.write("\n")
