from logging import getLogger
from typing import Any, Optional


class Block:
    def __init__(self, text: str, source: Optional[str] = None) -> None:
        self._text = text
        self._source = text if source is None else source

    def __eq__(self, other: Any) -> bool:
        logger = getLogger("comprehemd")

        if not isinstance(other, type(self)):
            logger.debug("%s is not the same type as %s", other, self)
            return False

        if self.text != other.text:
            logger.debug("%s is not equal to %s", self.text, other.text)
            return False

        if self.source != other.source:
            logger.debug("%s is not equal to %s", self.source, other.source)
            return False

        logger.debug("%s is equal to %s", self, other)
        return True

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(source={self.text}, text={self.text})"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.text}"

    @property
    def text(self) -> str:
        return self._text

    @property
    def trailing_empty_lines(self) -> int:
        for i, c in enumerate(reversed(self.text)):
            if c != "\n":
                return i
        return len(self.text)

    @property
    def source(self) -> str:
        return self._source

    def append_text(self, text: str) -> None:
        getLogger("comprehemd").debug('Appending "%s" to text "%s"', text, self._text)
        self._text += text

    def append_source(self, source: str) -> None:
        getLogger("comprehemd").debug(
            'Appending "%s" to source "%s"', source, self._source
        )
        self._source += source

    def collapse_text(self) -> None:
        self._text = self._text.rstrip()

    def collapse_source(self) -> None:
        self._source = self._source.rstrip() + "\n"
