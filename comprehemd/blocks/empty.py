from comprehemd.blocks.block import Block


class EmptyBlock(Block):
    def __init__(self) -> None:
        super().__init__(text="")

    def __repr__(self) -> str:
        return self.__class__.__name__

    def __str__(self) -> str:
        return self.__class__.__name__
