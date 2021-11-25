from comprehemd.code_patterns.base import CodePattern


class IndentPattern(CodePattern):
    @property
    def clean_expression(self) -> str:
        """
        Gets the regular expression that reveals the content of a line from its
        markup.
        """

        return "^[ ]{4}([^\\s].*)$"

    @property
    def end_expression(self) -> str:
        """
        Gets the regular expression that matches the end of this type of block.
        """

        return "^[ ]{0,3}[^\\s].*$"

    @property
    def fenced(self) -> bool:
        """
        Returns `True` if this type of code block has some pattern at the top
        and bottom of the block to indicate the content boundary.
        """

        return False

    @property
    def start_expression(self) -> str:
        """
        Gets the regular expression that matches the start of this type of
        block.
        """

        return "^[ ]{4}[^\\s].*$"
