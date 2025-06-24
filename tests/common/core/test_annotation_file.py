import pytest
from pathlib import Path
from annotation_parser.shape import Shape
from annotation_parser.core.annotation_file import AnnotationFile
from annotation_parser.adapters.adapter_factory import AdapterFactory


# --- DummyAdapter для универсальных тестов ---
class DummyAdapter:
    adapter_name = "dummy"

    @staticmethod
    def load(json_data, shift_point=None):
        # Просто возвращает одну фиктивную фигуру
        return (
            Shape(label="foo", coords=[[1, 2], [3, 4]], type="line"),
        )

    @staticmethod
    def shapes_to_json(original_json, shapes):
        # Примитивная сериализация
        return {"shapes": [s.label for s in shapes]}


@pytest.fixture(scope="module", autouse=True)
def register_dummy_adapter():
    AdapterFactory.register_adapter("dummy", DummyAdapter)
