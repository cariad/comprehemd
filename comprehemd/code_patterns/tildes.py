from comprehemd.code_patterns.base import CodePattern


class TildesPattern(CodePattern):
    @property
    def end_expression(self) -> str:
        return "^~~~$"

    @property
    def start_expression(self) -> str:
        return "^~~~(.*)$"

    @property
    def is_fenced(self) -> bool:
        return True
