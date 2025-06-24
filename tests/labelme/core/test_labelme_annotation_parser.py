import pytest
from shapely.geometry import Point

from annotation_parser.adapters.labelme_adapter import LabelMeAdapter
from annotation_parser.core.annotation_parser import AnnotationParser
from annotation_parser.public_enums import ShapeType
from annotation_parser.shape import Shape


@pytest.fixture
def labelme_shape_dict():
    return {
        "label": "cat",
        "points": [[100, 200], [150, 250]],
        "group_id": 42,
        "shape_type": "rectangle",
        "description": "test-shape",
        "flags": {"foo": "bar"},
        "mask": None,
    }


@pytest.fixture
def labelme_json(labelme_shape_dict):
    return {
        "shapes": [labelme_shape_dict],
        "imagePath": "test.png",
        "imageHeight": 600,
        "imageWidth": 800,
    }


def test_parse_labelme_json(labelme_json):
    shapes = AnnotationParser.parse(labelme_json, LabelMeAdapter)
    assert isinstance(shapes, tuple)
    assert len(shapes) == 1
    shape = shapes[0]
    assert isinstance(shape, Shape)
    assert shape.label == "cat"
    assert shape.type == ShapeType.RECTANGLE
    assert shape.number == 42
    assert shape.coords == [[100.0, 200.0], [150.0, 200.0], [150.0, 250.0], [100.0, 250.0]]  # auto rectangle
    assert shape.flags["foo"] == "bar"


def test_parse_labelme_with_shift_point(labelme_json):
    shift = Point(10, 20)
    shapes = AnnotationParser.parse(labelme_json, LabelMeAdapter, shift_point=shift)
    assert shapes[0].shift_point == shift
    shifted = shapes[0].shifted_coords
    # Each x/y must be reduced by shift.x/shift.y
    assert all(abs(x - (orig[0] - 10)) < 1e-6 and abs(y - (orig[1] - 20)) < 1e-6
               for (x, y), orig in zip(shifted, [[100, 200], [150, 200], [150, 250], [100, 250]]))


def test_parse_labelme_shape_invalid_type(labelme_json):
    # shape_type неизвестен
    labelme_json["shapes"][0]["shape_type"] = "hexagon"
    with pytest.raises(ValueError):
        AnnotationParser.parse(labelme_json, LabelMeAdapter)


def test_parse_labelme_json_missing_shapes():
    bad_json = {"not_shapes": []}
    with pytest.raises(ValueError):
        AnnotationParser.parse(bad_json, LabelMeAdapter)


def test_parse_labelme_shape_missing_fields(labelme_shape_dict):
    # Нет group_id, description, flags, mask
    minimal_shape = {
        "label": "dog",
        "points": [[10, 20], [30, 40]],
        "shape_type": "rectangle",
    }
    json_data = {"shapes": [minimal_shape]}
    shapes = AnnotationParser.parse(json_data, LabelMeAdapter)
    assert shapes[0].label == "dog"
    assert shapes[0].number is None
    assert shapes[0].description is None
    assert shapes[0].flags == {}
    assert shapes[0].coords == [[10.0, 20.0], [30.0, 20.0], [30.0, 40.0], [10.0, 40.0]]


def test_parse_labelme_shape_polygon_type():
    shape = {
        "label": "poly",
        "points": [[0, 0], [10, 0], [10, 10], [0, 10]],
        "shape_type": "polygon",
    }
    json_data = {"shapes": [shape]}
    shapes = AnnotationParser.parse(json_data, LabelMeAdapter)
    assert shapes[0].type == ShapeType.POLYGON
    assert shapes[0].coords == [[0.0, 0.0], [10.0, 0.0], [10.0, 10.0], [0.0, 10.0]]


def test_parse_labelme_shape_line_type():
    shape = {
        "label": "line",
        "points": [[1, 2], [3, 4]],
        "shape_type": "line",
    }
    json_data = {"shapes": [shape]}
    shapes = AnnotationParser.parse(json_data, LabelMeAdapter)
    assert shapes[0].type == ShapeType.LINE
    assert shapes[0].coords == [[1.0, 2.0], [3.0, 4.0]]
