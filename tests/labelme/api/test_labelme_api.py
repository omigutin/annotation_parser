import pytest

from annotation_parser.api.api import available_adapters, create
from annotation_parser.public_enums import Adapters
from annotation_parser.shape import Shape


@pytest.fixture
def minimal_labelme_json():
    # Минимальный валидный JSON в стиле labelme
    return {
        "shapes": [
            {
                "label": "cat",
                "points": [[1, 2], [3, 4]],
                "shape_type": "rectangle"
            }
        ]
    }


@pytest.fixture
def minimal_shape():
    # Минимальный Shape для labelme
    from annotation_parser.public_enums import ShapeType
    return Shape(label="cat", coords=[[1.0, 2.0], [3.0, 4.0]], type=ShapeType.RECTANGLE)


@pytest.fixture
def tmp_labelme_json_path(tmp_path, minimal_labelme_json):
    # Сохраняет минимальный labelme json во временный файл
    import json
    file = tmp_path / "labelme.json"
    with open(file, "w", encoding="utf-8") as f:
        json.dump(minimal_labelme_json, f)
    return str(file)


def test_available_adapters_labelme_present():
    adapters = available_adapters()
    assert Adapters.labelme.value in adapters


def test_create_and_parse_labelme(tmp_labelme_json_path, minimal_shape):
    parser = create(tmp_labelme_json_path, Adapters.labelme)
    assert hasattr(parser, "parse")
    shapes = parser.parse()
    assert isinstance(shapes, tuple)
    assert all(isinstance(s, type(minimal_shape)) for s in shapes)
    assert shapes[0].label == "cat"
