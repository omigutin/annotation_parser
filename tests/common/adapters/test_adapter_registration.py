import pytest

from annotation_parser.adapters.adapter_registration import AdapterRegistration
from annotation_parser.adapters.base_adapter import BaseAdapter


# Заглушечный адаптер
class MyTestAdapter(BaseAdapter, metaclass=AdapterRegistration):
    adapter_name = "my_test"

    @staticmethod
    def load(json_data, shift_point=None):
        return ()

    @staticmethod
    def shapes_to_json(original_json, shapes):
        return {}


def test_auto_registration():
    # Адаптер должен быть зарегистрирован автоматически по метаклассу
    assert "my_test" in AdapterRegistration.list_adapters()
    adapter = AdapterRegistration.get_adapter("my_test")
    assert adapter is MyTestAdapter


def test_case_insensitive_lookup():
    assert AdapterRegistration.get_adapter("MY_TEST") is MyTestAdapter
    assert AdapterRegistration.get_adapter("my_TEST") is MyTestAdapter


def test_register_adapter_manual():
    class ManualAdapter(BaseAdapter):
        adapter_name = "manual"
        @staticmethod
        def load(json_data, shift_point=None): return ()
        @staticmethod
        def shapes_to_json(original_json, shapes): return {}

    AdapterRegistration.register_adapter("manual", ManualAdapter)
    assert "manual" in AdapterRegistration.list_adapters()
    assert AdapterRegistration.get_adapter("manual") is ManualAdapter


def test_get_adapter_not_registered():
    with pytest.raises(ValueError):
        AdapterRegistration.get_adapter("nonexistent")


def test_list_adapters():
    adapters = AdapterRegistration.list_adapters()
    assert isinstance(adapters, list)
    assert "my_test" in adapters
