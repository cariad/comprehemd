from enum import Enum, auto, unique


@unique
class Fence(Enum):
    BACKTICKS = auto()
    TILDES = auto()
