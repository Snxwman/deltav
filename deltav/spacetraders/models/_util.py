# pyright: reportAny=false
from __future__ import annotations

from enum import Enum, EnumType
from types import UnionType
from typing import Any, get_args, get_origin

from pydantic import ValidationError, ValidatorFunctionWrapHandler, field_serializer, field_validator
from pydantic_core.core_schema import FieldValidationInfo


def validate_enum_by_name():

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
                _enum = None
                _ann = cls.__annotations__[info.field_name]

                print(f'{_ann=}')
                print(f'{isinstance(_ann, type)=}')
                print(f'{isinstance(_ann, type) and issubclass(_ann, Enum)=}')
                print(f'{get_origin(_ann)=}')
                if get_origin(_ann) is not None:
                    enum_types: list[type[Enum]] = [
                        _type
                        for _type in get_args(_ann)
                        if isinstance(_type, type) and issubclass(_type, Enum)
                    ]
                    if len(enum_types) > 1:
                        msg = f"Multiple Enum types in annotation: '{info.field_name}: {_ann}'"
                        raise TypeError(msg) from err
                    _enum = enum_types[0]

                if isinstance(_ann, type) and issubclass(_ann, Enum):
                    _enum = _ann

                if _enum is not None:
                    try:
                        return handler(_enum[value])
                    except (KeyError, ValueError):
                        msg = f"Invalid Enum name '{value}' for '{_enum.__name__}'"
                        raise ValueError(msg) from err
            raise

    return _validate_enum_by_name


def serialize_enum_by_name():

    @field_serializer('*', return_type=str, when_used='always')
    def _serialize_enum_by_name(value: Any) -> Any:
        if isinstance(value, Enum):
            return value.name
        return value

    return _serialize_enum_by_name
