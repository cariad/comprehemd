from logging import getLogger
from typing import List, Optional, Tuple

from comprehemd.code_patterns.backticks import BackticksPattern
from comprehemd.code_patterns.base import CodePattern
from comprehemd.code_patterns.indent import IndentPattern
from comprehemd.code_patterns.tildes import TildesPattern

code_patterns: List[CodePattern] = [
    BackticksPattern(),
    TildesPattern(),
    IndentPattern(),
]


def get_code_pattern(line: str) -> Tuple[Optional[CodePattern], Optional[str]]:
    """
    Gets the code pattern for the type of code block that `line` opens.

    Arguments:
        line: Line to check.

    Returns:
        Code pattern and language (if known) if the line starts a code block,
        otherwise `None` and `None`.
    """

    logger = getLogger("comprehemd")

    for pattern in code_patterns:
        found, language = pattern.is_start(line)
        if found:
            logger.debug(
                'Line "%s" matched by code pattern "%s" with language "%s"',
                line.rstrip(),
                pattern,
                language,
            )
            return pattern, language

    logger.debug('Line "%s" did not match any code patterns', line)
    return None, None


__all__ = [
    "BackticksPattern",
    "CodePattern",
    "IndentPattern",
    "TildesPattern",
]
