import pytest
from annotation_parser.adapters.base_adapter import BaseAdapter


# Минимальный dummy Shape для теста (не нужен полностью — только для _get_field)
class DummyObj:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.model_extra = kwargs.get("model_extra", {})


def test_get_field_from_attr():
    obj = DummyObj(label="car", number=5)
    assert BaseAdapter._get_field(obj, "label") == "car"
    assert BaseAdapter._get_field(obj, "number") == 5


def test_get_field_from_model_extra():
    obj = DummyObj(model_extra={"score": 0.98, "foo": 1})
    assert BaseAdapter._get_field(obj, "score") == 0.98
    assert BaseAdapter._get_field(obj, "foo") == 1


def test_get_field_not_found_returns_default():
    obj = DummyObj()
    assert BaseAdapter._get_field(obj, "not_exist") is None
    assert BaseAdapter._get_field(obj, "not_exist", default=123) == 123


def test_load_abstract():
    # Прямой вызов абстрактного метода должен вызывать NotImplementedError
    class Dummy(BaseAdapter):
        pass
    with pytest.raises(NotImplementedError):
        Dummy.load({}, None)


def test_shapes_to_json_abstract():
    # Прямой вызов абстрактного метода должен вызывать NotImplementedError
    class Dummy(BaseAdapter):
        pass
    with pytest.raises(NotImplementedError):
        Dummy.load({}, None)
