from typing import Type


class DomainModelRegistry:
    models: dict[str, Type] = {}

    @classmethod
    def register(cls, target: Type) -> None:
        DomainModelRegistry.models[target.__name__] = type

    @classmethod
    def get(cls, type_name: str) -> Type:
        return DomainModelRegistry.models[type_name]
