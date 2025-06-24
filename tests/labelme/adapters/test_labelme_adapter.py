import numpy as np
import pytest
import json
from pathlib import Path
from shapely.geometry import Point

from annotation_parser.adapters.labelme_adapter import LabelMeAdapter
from annotation_parser.shape import Shape
from annotation_parser.public_enums import ShapeType
from annotation_parser.types import ShiftPointType

LABELME_TEST_JSON_PATH = Path(__file__).parent.parent / "labelme_test.json"


@pytest.fixture
def labelme_json():
    """Загрузка тестового файла LabelMe JSON."""
    with open(LABELME_TEST_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def test_load_labelme_shapes(labelme_json):
    """Проверяет парсинг фигур из LabelMe JSON."""
    shapes = LabelMeAdapter.load(labelme_json)
    assert isinstance(shapes, tuple)
    assert all(isinstance(s, Shape) for s in shapes)
    assert len(shapes) > 0
    for shape in shapes:
        assert isinstance(shape.label, str)
        assert isinstance(shape.coords, list)
        assert isinstance(shape.type, ShapeType)


def test_load_with_shift_point(labelme_json):
    """Проверяет корректность смещения координат через shift_point."""
    shift = Point(10, 20)
    shapes = LabelMeAdapter.load(labelme_json, shift_point=shift)
    shapes_raw = LabelMeAdapter.load(labelme_json)
    for s, s_raw in zip(shapes, shapes_raw):
        shifted = [[x - shift.x, y - shift.y] for x, y in s_raw.coords]
        assert s.shift_point == shift
        assert s.shifted_coords == shifted


def test_load_invalid_json():
    """Проверяет, что некорректный JSON вызывает ValueError."""
    bad_json = {"foo": "bar"}
    with pytest.raises(ValueError):
        LabelMeAdapter.load(bad_json)


def test_shape_to_json_and_back(labelme_json):
    """Проверяет идемпотентность: shape -> json -> shape."""
    shapes = LabelMeAdapter.load(labelme_json)
    out_json = LabelMeAdapter.shapes_to_json(labelme_json, shapes)
    shapes2 = LabelMeAdapter.load(out_json)
    assert len(shapes) == len(shapes2)
    for s1, s2 in zip(shapes, shapes2):
        assert s1.label == s2.label
        assert s1.type == s2.type
        assert np.allclose(s1.coords, s2.coords)


def test_shape_to_json_fields(labelme_json):
    """Проверяет, что сохраняются все обязательные поля."""
    shapes = LabelMeAdapter.load(labelme_json)
    out_json = LabelMeAdapter.shapes_to_json(labelme_json, shapes)
    # Поля, которые обязательно должны быть
    required_fields = ["shapes", "imagePath", "imageWidth", "imageHeight", "flags", "version", "lineColor", "fillColor"]
    for field in required_fields:
        assert field in out_json


def test_supports_custom_fields(labelme_json):
    """Проверяет поддержку кастомных полей."""
    # Добавим поле position, которое обрабатывается в shape
    shape_dict = labelme_json["shapes"][0].copy()
    shape_dict["position"] = "left"
    test_json = dict(labelme_json)
    test_json["shapes"] = [shape_dict]
    shapes = LabelMeAdapter.load(test_json)
    assert hasattr(shapes[0], "position")
    assert shapes[0].position.value == "left"


def test_group_id_and_flags(labelme_json):
    """Проверяет поддержку group_id и flags."""
    shapes = LabelMeAdapter.load(labelme_json)
    for shape in shapes:
        assert hasattr(shape, "number")
        assert hasattr(shape, "flags")
        assert isinstance(shape.flags, dict)


def test_shapes_to_json_type_preserved(labelme_json):
    """Проверяет, что тип фигуры сохраняется корректно."""
    shapes = LabelMeAdapter.load(labelme_json)
    out_json = LabelMeAdapter.shapes_to_json(labelme_json, shapes)
    for shape_json in out_json["shapes"]:
        assert "shape_type" in shape_json
        assert shape_json["shape_type"] in [st.value for st in ShapeType]
