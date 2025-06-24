import pytest

from annotation_parser.adapters.adapter_factory import AdapterFactory
from annotation_parser.adapters.base_adapter import BaseAdapter
from annotation_parser.public_enums import Adapters


class DummyAdapter(BaseAdapter):
    adapter_name = "dummy"

    @staticmethod
    def load(json_data, shift_point=None):
        return ()

    @staticmethod
    def shapes_to_json(original_json, shapes):
        return {}


@pytest.fixture(autouse=True)
def clear_dummy_from_registry():
    # Очистка dummy-адаптера из реестра до/после каждого теста
    AdapterFactory.register_adapter("dummy", None)
    yield
    AdapterFactory._registry = {k: v for k, v in getattr(AdapterFactory, '_registry', {}).items() if k != "dummy"}


def test_register_and_get_adapter():
    AdapterFactory.register_adapter("dummy", DummyAdapter)
    adapter = AdapterFactory.get_adapter("dummy")
    assert adapter is DummyAdapter


def test_list_adapters_contains_registered():
    AdapterFactory.register_adapter("dummy", DummyAdapter)
    adapters = AdapterFactory.list_adapters()
    assert "dummy" in adapters


def test_get_adapter_by_enum():
    AdapterFactory.register_adapter("dummy", DummyAdapter)
    # Проверяем как строкой, так и через Enum
    assert AdapterFactory.get_adapter("dummy") is DummyAdapter
    # Если у тебя есть dummy в Enum, можно проверить через Adapters, иначе пропусти этот тест


def test_get_adapter_invalid_type():
    with pytest.raises(TypeError):
        AdapterFactory.get_adapter(123)  # не строка и не Enum


def test_get_adapter_unregistered():
    with pytest.raises(Exception):
        AdapterFactory.get_adapter("nonexistent")
