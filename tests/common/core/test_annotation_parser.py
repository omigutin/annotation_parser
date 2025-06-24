import pytest
from annotation_parser.core.annotation_parser import AnnotationParser
from annotation_parser.shape import Shape


class DummyAdapter:
    """Mock adapter for testing AnnotationParser."""
    adapter_name = "dummy"

    @staticmethod
    def load(json_data, shift_point=None):
        # shift_point для теста не важен, но можно проверить что он прокидывается
        return (Shape(label="a", coords=[[1, 2]], type="point"),)


@pytest.mark.parametrize("json_data", [
    {"key": "value"},
    {"foo": "bar"},
    [{"shapes": []}],  # список вместо dict — допустимо
])
def test_adapter_load_is_called(json_data):
    shapes = AnnotationParser.parse(json_data, DummyAdapter)
    assert isinstance(shapes, tuple)
    assert len(shapes) == 1
    assert shapes[0].label == "a"


def test_shift_point_is_passed():
    # Проверим что shift_point пробрасывается в адаптер
    captured = {}
    class CapturingAdapter(DummyAdapter):
        @staticmethod
        def load(json_data, shift_point=None):
            captured["shift_point"] = shift_point
            return (Shape(label="b", coords=[[3, 4]], type="point"),)
    AnnotationParser.parse({"k": 1}, CapturingAdapter, shift_point=(123, 456))
    assert captured["shift_point"] == (123, 456)


def test_adapter_without_load_raises():
    class BadAdapter: pass
    with pytest.raises(ValueError) as e:
        AnnotationParser.parse({}, BadAdapter)
    assert "does not implement 'load'" in str(e.value)


def test_adapter_returns_not_iterable_raises():
    class BadAdapter:
        @staticmethod
        def load(json_data, shift_point=None):
            return "not a list or tuple"
    with pytest.raises(ValueError) as e:
        AnnotationParser.parse({}, BadAdapter)
    assert "returned unsupported type" in str(e.value)
