import pytest

from annotation_parser.adapters.adapter_registration import AdapterRegistration
from annotation_parser.adapters.labelme_adapter import LabelMeAdapter


def test_labelme_adapter_auto_registered():
    """LabelMeAdapter должен автоматически регистрироваться через метакласс."""
    adapters = AdapterRegistration.list_adapters()
    assert "labelme" in adapters

    # Должен возвращать именно LabelMeAdapter
    adapter_cls = AdapterRegistration.get_adapter("labelme")
    assert adapter_cls is LabelMeAdapter


def test_adapter_registration_case_insensitive():
    """Регистрация и получение адаптеров должны работать независимо от регистра."""
    adapter_cls1 = AdapterRegistration.get_adapter("LaBeLmE")
    adapter_cls2 = AdapterRegistration.get_adapter("LABELME")
    assert adapter_cls1 is LabelMeAdapter
    assert adapter_cls2 is LabelMeAdapter


def test_register_and_get_new_adapter():
    """Можно вручную зарегистрировать новый адаптер и получить его."""
    class DummyAdapter:
        pass

    AdapterRegistration.register_adapter("labelme_dummy2", DummyAdapter)
    result = AdapterRegistration.get_adapter("labelme_dummy2")
    assert result is DummyAdapter


def test_get_adapter_not_found():
    """Попытка получить несуществующий адаптер вызывает ValueError."""
    with pytest.raises(ValueError):
        AdapterRegistration.get_adapter("no_such_adapter")
