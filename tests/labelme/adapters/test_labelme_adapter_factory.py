import pytest

from annotation_parser.adapters.adapter_factory import AdapterFactory
from annotation_parser.adapters.labelme_adapter import LabelMeAdapter
from annotation_parser.public_enums import Adapters


def test_labelme_adapter_is_registered():
    """LabelMe-адаптер должен быть зарегистрирован и доступен по имени и enum."""
    # Через строку
    adapter_cls_str = AdapterFactory.get_adapter("labelme")
    assert adapter_cls_str is LabelMeAdapter

    # Через enum
    adapter_cls_enum = AdapterFactory.get_adapter(Adapters.labelme)
    assert adapter_cls_enum is LabelMeAdapter

    # Через list_adapters
    all_adapters = AdapterFactory.list_adapters()
    assert "labelme" in all_adapters


def test_labelme_adapter_case_insensitive():
    """Доступ к адаптеру должен быть регистронезависимым."""
    adapter_cls = AdapterFactory.get_adapter("LaBeLmE")
    assert adapter_cls is LabelMeAdapter


def test_labelme_adapter_not_found():
    """Попытка получить несуществующий адаптер приводит к ValueError."""
    with pytest.raises(ValueError):
        AdapterFactory.get_adapter("unknown_adapter")


def test_register_new_labelme_adapter(monkeypatch):
    """Регистрация нового адаптера по имени."""
    class DummyAdapter:
        pass

    AdapterFactory.register_adapter("labelme_dummy", DummyAdapter)
    assert AdapterFactory.get_adapter("labelme_dummy") is DummyAdapter
