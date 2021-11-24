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
        return f"{self.__class__.__name__}(language={self.language or '<None>'}, source={self.text}, text={self.text})"

    def __str__(self) -> str:
        return f"{self.__class__.__name__} ({self.language or '<None>'}): {self.text}"

    @property
    def language(self) -> Optional[str]:
        return self._language

    def render(self, writer: IO[str], fence: Fence = Fence.BACKTICKS) -> None:
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
