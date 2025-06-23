__all__ = ['AdapterFactory']

from typing import List, Union

from ..public_enums import Adapters
from .adapter_registration import AdapterRegistration
from .base_adapter import AdapterType


class AdapterFactory:
    """
        Публичная фасадная точка для работы с адаптерами разметки.
    """

    @staticmethod
    def register_adapter(name: str, adapter: AdapterType) -> None:
        AdapterRegistration.register_adapter(name, adapter)

    @staticmethod
    def list_adapters() -> List[str]:
        return AdapterRegistration.list_adapters()

    @staticmethod
    def get_adapter(markup_type: Union[str, Adapters]) -> AdapterType:
        if isinstance(markup_type, str):
            key = markup_type
        elif isinstance(markup_type, Adapters):
            key = markup_type.name
        else:
            raise TypeError(f"markup_type must be str or Adapters, not {type(markup_type).__name__}")
        return AdapterRegistration.get_adapter(key)
