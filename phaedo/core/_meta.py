from .fields import Field, ListField


class DomainMeta(type):
    def __new__(mcs, cls, bases, attrs):
        fields = []
        for attribute_name, field in attrs.items():
            if issubclass(type(field), Field) or issubclass(type(field), ListField):
                field.set_attribute_name(attribute_name)
                fields.append(field)
        attrs['fields'] = fields
        return super().__new__(mcs, cls, bases, attrs)
