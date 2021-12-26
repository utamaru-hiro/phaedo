import hashlib
from ._meta import DomainMeta
from ._registry import DomainModelRegistry


class DomainModel(metaclass=DomainMeta):
    def __new__(cls):
        DomainModelRegistry.register(cls)
        this = super().__new__(cls)
        this.__data__ = {}
        for field in cls.__dict__['fields']:
            attribute_name = field.get_attribute_name()
            default_value = field.default_value()
            if default_value is not None:
                this.__data__[attribute_name] = default_value

        return this

    def loads(self, data: dict) -> None:
        for field in self.__class__.__dict__['fields']:
            if not field.can_load():
                continue

            attribute_name = field.get_attribute_name()
            value = data.get(attribute_name, None)
            if value is None:
                setattr(self, attribute_name, None)
                continue

            field_type = field.get_type()
            if issubclass(field_type, DomainModel):
                if field.is_list():
                    setattr(self, attribute_name, [DomainModel._generate(field_type, element) for element in value])
                else:
                    setattr(self, attribute_name, DomainModel._generate(field_type, value))
            else:
                setattr(self, attribute_name, value)

    @staticmethod
    def _generate(field_type, data):
        instance = super().__new__(field_type)
        instance.__data__ = {}
        for field in field_type.__dict__['fields']:
            attribute_name = field.get_attribute_name()
            default_value = field.default_value()
            if default_value is not None:
                instance.__data__[attribute_name] = default_value

        instance.loads(data)
        return instance

    def dumps(self) -> dict:
        res = {}
        for field in self.__class__.__dict__['fields']:
            if not field.can_dump():
                continue

            attribute_name = field.get_attribute_name()
            value = getattr(self, attribute_name)
            if isinstance(value, list):
                res[attribute_name] = [self._evaluate(element) for element in value]
            else:
                res[attribute_name] = self._evaluate(value)
        return res

    @staticmethod
    def _evaluate(v):
        return v.dumps() if isinstance(v, DomainModel) else v

    @classmethod
    def force_construct(cls, data: dict):
        instance = cls.__new__(cls)
        for field in cls.__dict__['fields']:
            attribute_name = field.get_attribute_name()
            value = data.get(attribute_name, None)
            if value is None:
                instance.__data__[attribute_name] = None
                continue

            field_type = field.get_type()
            if issubclass(field_type, DomainModel):
                if field.is_list():
                    instance.__data__[attribute_name] = [field_type.force_construct(element) for element in value]
                else:
                    instance.__data__[attribute_name] = field_type.force_construct(value)
            else:
                instance.__data__[attribute_name] = value

        return instance

    def __str__(self) -> str:
        class_name = self.__class__.__name__
        attributes = []
        for field in self.__class__.__dict__['fields']:
            attribute_name = field.get_attribute_name()
            value = getattr(self, attribute_name)
            if isinstance(value, list):
                str_value = ', '.join([str(element) for element in value])
                value = f'[{str_value}]'
            attributes.append(f'{attribute_name}={value}')
        inner_data = ', '.join(attributes)
        return f'{class_name}({inner_data})'

    def __hash__(self) -> int:
        return int(hashlib.sha256(str(self).encode()).hexdigest(), 16)

    def __eq__(self, __o: object) -> bool:
        if self.__class__ != __o.__class__:
            return False

        attributes = frozenset([field.get_attribute_name() for field in self.__class__.__dict__['fields']])
        for attribute in attributes:
            value = getattr(self, attribute)
            o_value = getattr(__o, attribute)
            if value != o_value:
                return False

        return True
