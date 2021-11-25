from logging import getLogger
from typing import Any, Optional


class Block:
    """
    The base of all parsed blocks.

    Arguments:
        text:   Meaningful text content.
        source: Original Markdown source. Defaults to the text value.
    """

    def __init__(self, text: str, source: Optional[str] = None) -> None:
        self._text = text
        self._logger = getLogger("comprehemd")
        self._source = text if source is None else source

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, type(self)):
            self._logger.debug(
                "%s vs %s: type %s != %s",
                repr(other),
                repr(self),
                other.__class__,
                self.__class__,
            )
            return False

        if self.text != other.text:
            self._logger.debug(
                '%s vs %s: text "%s" != "%s"',
                repr(other),
                repr(self),
                other.escaped_text,
                self.escaped_text,
            )
            return False

        if self.source != other.source:
            self._logger.debug(
                '%s vs %s: source "%s" != "%s"',
                repr(other),
                repr(self),
                other.escaped_source,
                self.escaped_source,
            )
            return False

        self._logger.debug("%s vs %s: equal", self, other)
        return True

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}("{self.escaped_text}", source="{self.escaped_source}")'

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.escaped_text}"

    def append_source(self, source: str) -> None:
        """
        Appends `source` to the source value.

        Arguments:
            source: Source to append.
        """

        self._logger.debug(
            'Appending "%s" to source "%s"',
            self.escape(source),
            self.escaped_source,
        )
        self._source += source

    def append_text(self, text: str) -> None:
        """
        Appends `text` to the text value.

        Arguments:
            text: Text to append.
        """

        self._logger.debug(
            'Appending "%s" to text "%s"',
            self.escape(text),
            self.escaped_text,
        )
        self._text += text

    def collapse_text(self) -> None:
        """
        Collapses any trailing whitespace in the text.
        """

        self._text = self._text.rstrip()

    def collapse_source(self) -> None:
        """
        Collapses any trailing whitespace in the source to a single new line.
        """

        self._source = self._source.rstrip() + "\n"

    @staticmethod
    def escape(value: str) -> str:
        """
        Transforms `value` to make control characters visible.

        Arguments:
            value: Text to transform.

        Returns:
            Value with visible control characters.
        """

        return value.replace("\n", "\\n")

    @property
    def escaped_source(self) -> str:
        """
        Gets the source with visible control characters.
        """

        return self.escape(self.source)

    @property
    def escaped_text(self) -> str:
        """
        Gets the text with visible control characters.
        """

        return self.escape(self.text)

    @property
    def source(self) -> str:
        """
        Gets the original source Markdown.
        """

        return self._source

    @property
    def text(self) -> str:
        """
        Gets the meaningful text content.
        """

        return self._text

    @property
    def trailing_new_lines(self) -> int:
        """
        Gets the count of trailing empty lines in the text.
        """

        for i, c in enumerate(reversed(self.text)):
            if c != "\n":
                return i
        return len(self.text)
