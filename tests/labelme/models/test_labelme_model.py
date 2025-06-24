import pytest
from pydantic import ValidationError

from annotation_parser.models.labelme_model import JsonLabelme, JsonLabelmeShape


def test_jsonlabelmeshape_valid_fields():
    shape = JsonLabelmeShape(
        label="person",
        points=[[10, 20], [30, 40]],
        shape_type="rectangle",
        group_id=1,
        description="Test desc",
        flags={"foo": True},
        mask=None
    )
    assert shape.label == "person"
    assert shape.shape_type == "rectangle"
    assert shape.points == [[10, 20], [30, 40]]
    assert shape.flags["foo"] is True


def test_jsonlabelmeshape_allows_extra():
    # Добавляем кастомное поле
    shape = JsonLabelmeShape(
        label="person",
        points=[[1, 2], [3, 4]],
        shape_type="point",
        extra_field="extra_value"
    )
    assert hasattr(shape, "model_extra")
    assert "extra_field" in shape.model_extra
    assert shape.model_extra["extra_field"] == "extra_value"


def test_jsonlabelme_defaults():
    # Создаём модель только с shapes
    shape = JsonLabelmeShape(label="a", points=[[1, 2]], shape_type="point")
    m = JsonLabelme(shapes=[shape])
    assert m.version == "5.5.0"
    assert m.imageHeight == 1080
    assert m.imageWidth == 1920
    assert isinstance(m.shapes, list)
    assert m.shapes[0].label == "a"


def test_jsonlabelme_shape_list_validation():
    # Проверка: пустой список shapes допустим
    m = JsonLabelme(shapes=[])
    assert m.shapes == []


def test_jsonlabelme_extra_fields():
    # Модель поддерживает произвольные поля (через model_extra)
    m = JsonLabelme(shapes=[], foo="bar")
    assert hasattr(m, "model_extra")
    assert m.model_extra["foo"] == "bar"


def test_jsonlabelmeshape_invalid_shape_type():
    # Некорректный shape_type приводит к ошибке
    with pytest.raises(Exception):
        JsonLabelmeShape(label="a", points=[[1, 2]], shape_type=None)


def test_jsonlabelmeshape_points_required():
    with pytest.raises(ValidationError):
        JsonLabelmeShape(label="test")


def test_jsonlabelme_dump_and_restore():
    # Проверяем сериализацию и восстановление
    shape = JsonLabelmeShape(label="a", points=[[1, 2]], shape_type="point")
    m = JsonLabelme(shapes=[shape])
    dct = m.model_dump()
    m2 = JsonLabelme.model_validate(dct)
    assert m2.shapes[0].label == "a"
    assert m2.imagePath == "cam.jpg"
