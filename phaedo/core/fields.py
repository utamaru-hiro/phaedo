from typing import (Callable, Generic, Optional, Type, TypeVar, Union)
from .validation import Validator, ValidationError
from ._registry import DomainModelRegistry


T = TypeVar('T')


class Field(Generic[T]):
    def __init__(
            self,
            field_type: Union[str, Type[T]],
            name: str = None,
            validators: list[Validator] = None,
            converter: Callable[[Optional[T]], T] = None,
            load=True,
            dump=True,
            default: T = None
    ) -> None:
        self._field_type = field_type
        self._name = name
        self._validators = validators
        self._converter = converter
        self._load = load
        self._dump = dump
        self._default = default
        self._attribute_name = None

    def set_attribute_name(self, attribute_name: str) -> None:
        self._attribute_name = attribute_name

    def get_attribute_name(self) -> str:
        return self._attribute_name

    def get_type(self) -> Type:
        if isinstance(self._field_type, str):
            return DomainModelRegistry.get(self._field_type)

        return self._field_type

    @staticmethod
    def is_list() -> bool:
        return False

    def can_load(self) -> bool:
        return self._load

    def can_dump(self) -> bool:
        return self._dump

    def default_value(self) -> Optional[T]:
        return self._default

    def __get__(self, obj, obj_type=None) -> T:
        return obj.__data__.get(self._attribute_name, None)

    def __set__(self, obj, value: Optional[T]) -> None:
        if self._validators is not None:
            key = self._name if self._name is not None else self._attribute_name
            for validator in self._validators:
                if not validator.validate(value):
                    raise ValidationError(key, validator.message())

        if self._converter is not None:
            obj.__data__[self._attribute_name] = self._converter(value)
        else:
            obj.__data__[self._attribute_name] = value


class ListField(Generic[T]):
    def __init__(
            self,
            field_type: Union[str, Type[T]],
            name: str = None,
            validators: list[Validator] = None,
            converter: Callable[[Optional[T]], T] = None,
            load=True,
            dump=True,
            default: list[T] = None
    ) -> None:
        self._field_type = field_type
        self._name = name
        self._validators = validators
        self._converter = converter
        self._load = load
        self._dump = dump
        self._default = default
        self._attribute_name = None

    def set_attribute_name(self, attribute_name: str):
        self._attribute_name = attribute_name

    def get_attribute_name(self):
        return self._attribute_name

    def get_type(self) -> Type:
        if isinstance(self._field_type, str):
            return DomainModelRegistry.get(self._field_type)

        return self._field_type

    @staticmethod
    def is_list() -> bool:
        return True

    def can_load(self) -> bool:
        return self._load

    def can_dump(self) -> bool:
        return self._dump

    def default_value(self) -> Optional[list[T]]:
        return self._default

    def __get__(self, obj, obj_type=None) -> list[T]:
        return obj.__data__.get(self._attribute_name, None)

    def __set__(self, obj, value: Optional[list[T]]) -> None:
        attribute_value_list: list[T] = []
        if value is not None:
            for element in value:
                if self._validators is not None:
                    key = self._name if self._name is not None else self._attribute_name
                    for validator in self._validators:
                        if not validator.validate(value):
                            raise ValidationError(key, validator.message())

                if self._converter is not None:
                    attribute_value_list.append(self._converter(element))
                else:
                    attribute_value_list.append(element)

            obj.__data__[self._attribute_name] = attribute_value_list
