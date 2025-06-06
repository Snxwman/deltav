from enum import Enum, auto

from deltav.spacetraders.enums import serialize_by_name


@serialize_by_name
class ContractType(Enum):
    """

    PROCUREMENT
    SHUTTLE
    TRANSPORT
    """

    PROCUREMENT = auto()
    SHUTTLE = auto()
    TRANSPORT = auto()
