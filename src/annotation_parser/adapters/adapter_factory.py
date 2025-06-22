__all__ = ['AdapterFactory']

from typing import Type, List

from ..public_enums import Adapters
from .base_adapter import BaseAdapter


class AdapterFactory:
    """
        Унифицированная фабрика для поиска, регистрации и получения нужного адаптера по формату.
        Работает через внутренний реестр, который можно расширять во время выполнения.
    """
    _registry: dict[str, Type[BaseAdapter]] = {}

    @classmethod
    def register_adapter(cls, name: str, adapter: Type[BaseAdapter]) -> None:
        """ Регистрирует адаптер для указанного формата (переопределяет, если такой уже был). """
        cls._registry[name.lower()] = adapter

    @classmethod
    def list_adapters(cls) -> List[str]:
        """ Список всех зарегистрированных адаптеров (ключей форматов). """
        return list(cls._registry.keys())

    @classmethod
    def get_adapter(cls, markup_type: str | Adapters) -> Type[BaseAdapter]:
        """
            Унифицированный способ получить класс-адаптер по типу разметки.
            Args:
                markup_type: Название ('labelme', 'coco', ...) или Enum Adapters.
            Returns:
                Класс-адаптер.
            Raises:
                ValueError: Если адаптер не зарегистрирован.
                TypeError: Если передан некорректный тип.
        """
        if isinstance(markup_type, str):
            key = markup_type.lower()
        elif isinstance(markup_type, Adapters):
            key = markup_type.name.lower()
        else:
            raise TypeError(f"markup_type must be str or Adapters, not {type(markup_type).__name__}")

        try:
            return cls._registry[key]
        except KeyError:
            raise ValueError(f'Adapter "{key}" is not registered. '
                             f'Available: {", ".join(cls._registry.keys())}')
