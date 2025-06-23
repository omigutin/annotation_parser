__all__ = ['AdapterRegistration']

from abc import ABCMeta
from typing import Dict

from .base_adapter import AdapterType


class AdapterRegistration(ABCMeta):
    """
        Метакласс для автоматической регистрации адаптеров разметки.
        Все адаптеры с объявленным adapter_name автоматически добавляются в реестр.
        Позволяет получать адаптеры по имени и вручную регистрировать новые.
        Samples:
            class MyAdapter(BaseAdapter, metaclass=AdapterRegistration):
                adapter_name = "my"
                ...
    """

    _registry: Dict[str, AdapterType] = {}

    def __new__(mcs, name, bases, namespace, **kwargs):
        cls = super().__new__(mcs, name, bases, namespace)
        adapter_name = namespace.get("adapter_name")
        if adapter_name:
            mcs._registry[adapter_name.lower()] = cls
        return cls

    @classmethod
    def list_adapters(cls) -> list[str]:
        """
            Возвращает список всех зарегистрированных адаптеров.
            Returns:
                List[str]: Список имён.
        """
        return list(cls._registry.keys())

    @classmethod
    def get_adapter(cls, name: str) -> AdapterType:
        """
            Получить адаптер по имени (case-insensitive).
            Args:
                name (str): Имя адаптера.
            Returns:
                AdapterType: Класс-адаптер.
            Raises:
                ValueError: Если адаптер не зарегистрирован.
        """
        key = name.lower()
        if key not in cls._registry:
            raise ValueError(f'Adapter "{key}" is not registered. Available: {", ".join(cls._registry.keys())}')
        return cls._registry[key]

    @classmethod
    def register_adapter(cls, name: str, adapter: AdapterType) -> None:
        """
            Вручную зарегистрировать адаптер.
            Args:
                name (str): Имя.
                adapter (BaseAdapter): Класс-адаптер.
        """
        cls._registry[name.lower()] = adapter
