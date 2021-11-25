from comprehemd.code_patterns.base import CodePattern


class BackticksPattern(CodePattern):
    @property
    def end_expression(self) -> str:
        """
        Gets the regular expression that matches the end of this type of block.
        """

        return "^```$"

    @property
    def fenced(self) -> bool:
        """
        Returns `True` if this type of code block has some pattern at the top
        and bottom of the block to indicate the content boundary.
        """

        return True

    @property
    def start_expression(self) -> str:
        """
        Gets the regular expression that matches the start of this type of
        block.
        """

        return "^```(.*)$"
