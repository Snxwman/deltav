from enum import Enum
from typing import Annotated, TypeVar

from pydantic import BeforeValidator, PlainSerializer


T = TypeVar('T')


# https://stackoverflow.com/a/79389411
def serialize_by_name(enum_type: type[T]) -> type[T]:
    if issubclass(enum_type, Enum):
        return Annotated[
            enum_type,
            BeforeValidator(  # If you want to deserialize by name
                lambda member: member if isinstance(member, enum_type) else enum_type[member]
            ),
            PlainSerializer(  # If you want to serialize by name
                lambda member: member.name, return_type='str', when_used='always'
            ),
        ]  # pyright: ignore[reportReturnType]
    else:
        raise TypeError
