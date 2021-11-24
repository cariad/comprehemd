from comprehemd.code_patterns.base import CodePattern


class IndentPattern(CodePattern):

    #######################################################

    @property
    def clean_expression(self) -> str:
        return "^[ ]{4}([^\\s].*)$"

    @property
    def end_expression(self) -> str:
        return "^[ ]{0,3}[^\\s].*$"

    @property
    def start_expression(self) -> str:
        return "^[ ]{4}[^\\s].*$"

    @property
    def include_start(self) -> bool:
        return True

    @property
    def collapse(self) -> bool:
        return True

    @property
    def is_fenced(self) -> bool:
        return False
