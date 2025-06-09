from enum import Enum, auto

from deltav.spacetraders.enums import serialize_by_name


@serialize_by_name 
class SystemType(Enum):
    """

    BLACK_HOLE
    BLUE_STAR
    HYPERGIANT
    NEBULA
    NEUTRON_STAR
    ORANGE_STAR
    RED_STAR
    UNSTABLE
    WHITE_DWARF
    YOUNG_STAR
    """

    BLACK_HOLE = auto()
    BLUE_STAR = auto()
    HYPERGIANT = auto()
    NEBULA = auto()
    NEUTRON_STAR = auto()
    ORANGE_STAR = auto()
    RED_STAR = auto()
    UNSTABLE = auto()
    WHITE_DWARF = auto()
    YOUNG_STAR = auto()
