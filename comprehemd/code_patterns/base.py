from abc import ABC, abstractproperty
from re import match
from typing import Optional, Tuple


class CodePattern(ABC):
    """
    Abstract base class for all types of code block.
    """

    def __str__(self) -> str:
        return self.__class__.__name__

    def clean(self, line: str) -> str:
        """
        Reveals the content of a line from its markup.

        Arguments:
            line: Line to clean.

        Returns:
            Line content.
        """

        if not self.clean_expression:
            return line

        if m := match(self.clean_expression, line):
            return m.group(1) if len(m.groups()) > 0 else line

        return line

    @property
    def clean_expression(self) -> Optional[str]:
        """
        Gets the regular expression that reveals the content of a line from its
        markup.
        """

        return None

    @abstractproperty
    def end_expression(self) -> str:
        """
        Gets the regular expression that matches the end of this type of block.
        """

    @abstractproperty
    def fenced(self) -> bool:
        """
        Returns `True` if this type of code block has some pattern at the top
        and bottom of the block to indicate the content boundary.
        """

    def is_end(self, line: str) -> bool:
        """
        Checks if `line` ends code blocks of this type.

        Arguments:
            line: Line to check

        Returns:
            `True` if `line` ends code blocks of this type.
        """

        return not not match(self.end_expression, line.rstrip())

    def is_start(self, line: str) -> Tuple[bool, Optional[str]]:
        """
        Checks if `line` starts a code block of this type.

        Arguments:
            line: Line to check.

        Returns:
            `True` and language if `line` starts a code block of this type.
        """

        if m := match(self.start_expression, line):
            lang = m.group(1) if len(m.groups()) > 0 else None
            return True, lang
        return False, None

    @abstractproperty
    def start_expression(self) -> str:
        """
        Gets the regular expression that matches the start of this type of
        block.
        """
