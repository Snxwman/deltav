# pyright: reportAny=false
from __future__ import annotations

from enum import Enum, EnumType
from pprint import pp
from pydoc import locate
from types import UnionType
from typing import Any, TypeVar, get_args, get_origin, override

from deepmerge import always_merger
from pydantic import (
    AliasGenerator,
    BaseModel,
    ConfigDict,
    SerializationInfo,
    ValidationError,
    ValidatorFunctionWrapHandler,
    field_serializer,
    field_validator,
)
from pydantic.alias_generators import to_camel
from pydantic_core.core_schema import FieldValidationInfo

from deltav.spacetraders.models._str import logfmt, pretty
from deltav.spacetraders.models._util import serialize_enum_by_name, validate_enum_by_name

# TODO: Look into the following model config fields for ConfigDict
#   - str_to_upper
#   - str_min_length
#   - str_max_length
#   - use_enum_values
#   - validate_assignment


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

    _enum_validator = validate_enum_by_name()
    _enum_serializer = serialize_enum_by_name()

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

    @field_validator('*', mode='wrap')
    @classmethod
    def _validate_enum_by_name(
        cls, value: Any, handler: ValidatorFunctionWrapHandler, info: FieldValidationInfo
    ) -> Any:
        try:
            return handler(value)
        except ValidationError as err:
            if info.field_name is None:
                msg = 'Cannot determine field name for enum validator'
                raise RuntimeError(msg) from err

            if err.errors()[0]['type'] == 'enum':
                _type = cls.__annotations__[info.field_name]
                _enum = None

                pp(info.field_name)
                pp(cls.__annotations__[info.field_name])
                pp(locate(f'deltav.spacetraders.enums.{_type}'))
                pp(locate(f'deltav.spacetraders.enums.faction.{_type}'))
                if get_origin(_type) is not None:
                    _enum_types = [
                        _sub_type
                        for _sub_type in get_args(_type)
                        if isinstance(_sub_type, type) and issubclass(_sub_type, Enum)
                    ]
                    if len(_enum_types) > 1:
                        msg = f"Multiple Enum types in annotation: '{info.field_name}: {_ann}'"
                        raise TypeError(msg) from err
                    _enum = _enum_types[0]
                    return handler(_enum[value])

                if isinstance(_type, type) and issubclass(_type, Enum):
                    _enum = _type
                    return handler(_type[value])
            else:
                raise

    # _enum_validator = validate_enum_by_name()
    _enum_serializer = serialize_enum_by_name()

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
