from abc import ABC, abstractproperty
from re import match
from typing import Optional, Tuple


class CodePattern(ABC):
    """
    Abstract base class for all types of code block.
    """

    ########################################################

    def __str__(self) -> str:
        return self.__class__.__name__

    def clean(self, line: str) -> str:
        # line = line.rstrip()

        if not self.clean_expression:
            return line

        if m := match(self.clean_expression, line):
            return m.group(1) if len(m.groups()) > 0 else line
        return line

    @property
    def clean_expression(self) -> Optional[str]:
        """Gets the regular expression that cleans a line."""
        return None

    @property
    def collapse(self) -> bool:
        return False

    @abstractproperty
    def end_expression(self) -> str:
        """Gets the regular expression that matches the end of this pattern."""

    @abstractproperty
    def start_expression(self) -> str:
        """Gets the regular expression that matches the start of this pattern."""

    @abstractproperty
    def is_fenced(self) -> bool:
        """..."""

    def is_end(self, line: str) -> bool:
        return not not match(self.end_expression, line.rstrip())

    ##############################

    def is_start(self, line: str) -> Tuple[bool, Optional[str]]:
        """
        Checks if `line` starts a code block of this type.

        Arguments:
            line: Line to check.

        Returns:
            `True` and language (if known) if the line starts a code block of
            this type, otherwise `False` and `None`.
        """

        if m := match(self.start_expression, line):
            lang = m.group(1) if len(m.groups()) > 0 else None
            return True, lang
        return False, None
