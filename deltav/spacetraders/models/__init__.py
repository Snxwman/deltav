# pyright: reportAny=false
from __future__ import annotations

from typing import TypeVar, override

from deepmerge import always_merger
from pydantic import AliasGenerator, BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from deltav.spacetraders.models._str import logfmt, pretty

# TODO: Look into the following model config fields for ConfigDict
#   - str_to_upper
#   - str_min_length
#   - str_max_length
#   - use_enum_values
#   - validate_assignment

# TODO: Find a way to validate an enum by field name


# Inherited super type used for type annotations
class SpaceTradersAPIReqShape(BaseModel):
    """Base class for all request data sent in an SpaceTraders API request.

    Inherits from pydantic.BaseModel.
    """

    model_config = ConfigDict(  # pyright: ignore[reportUnannotatedClassAttribute]
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        revalidate_instances='always',
        serialize_by_alias=True
    )  # fmt: skip

    @property
    def pretty(self) -> str:
        return pretty(self, 0).expandtabs(4)

    @property
    def logfmt(self) -> str:
        return logfmt(self)

    @override
    def __str__(self) -> str:
        return repr(self)


# Inherited super type used for type annotations
class SpaceTradersAPIResShape(BaseModel):
    """Base class for all response data received by a SpaceTraders API call.

    Inherits from pydantic.BaseModel.
    """

    model_config = ConfigDict(  # pyright: ignore[reportUnannotatedClassAttribute]
        alias_generator=to_camel,
        revalidate_instances='always',
        validate_by_alias=True,
    )  # fmt: skip

    @property
    def pretty(self) -> str:
        return pretty(self, 0).expandtabs(4)

    @property
    def logfmt(self) -> str:
        return logfmt(self)

    @override
    def __str__(self) -> str:
        return repr(self)


class NoDataReqShape(SpaceTradersAPIReqShape):
    pass


class NoDataResShape(SpaceTradersAPIResShape):
    pass


T = TypeVar('T', bound='SpaceTradersAPIResShape')


# https://github.com/pydantic/pydantic/discussions/3416
def merge_models(base: T, nxt: T) -> T:
    """Merge two Pydantic model instances.

    The attributes of 'base' and 'nxt' that weren't explicitly set are dumped into dicts
    using '.model_dump(exclude_unset=True)', which are then merged using 'deepmerge',
    and the merged result is turned into a model instance using '.model_validate'.

    For attributes set on both 'base' and 'nxt', the value from 'nxt' will be used in
    the output result.
    """

    base_dict = base.model_dump(exclude_unset=True)
    next_dict = nxt.model_dump(exclude_unset=True)
    merged_dict = always_merger.merge(base_dict, next_dict)
    return base.model_validate(merged_dict, by_name=True)
