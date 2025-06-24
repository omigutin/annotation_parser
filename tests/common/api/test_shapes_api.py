import pytest

from annotation_parser.api.shapes_api import (
    set_shift_point, get_shapes_by_label, get_shapes_by_number, get_shapes_by_wz_number
)
from annotation_parser.shape import Shape


def point_eq(p, exp):
    """
    Универсальное сравнение координаты (x, y) с ожидаемым tuple/list.
    Поддерживает tuple, list, namedtuple, объекты с атрибутами x/y, numpy, shapely Point и др.
    """
    if p is None or exp is None:
        return p is exp

    # tuple или list
    if isinstance(p, (tuple, list)) and len(p) == 2:
        return tuple(float(x) for x in p) == tuple(float(x) for x in exp)

    # .x и .y (shapely, namedtuple и пр.)
    if hasattr(p, "x") and hasattr(p, "y"):
        return (float(p.x), float(p.y)) == tuple(float(x) for x in exp)

    # .to_tuple() или .as_tuple()
    for meth in ("to_tuple", "as_tuple"):
        if hasattr(p, meth):
            return tuple(float(x) for x in getattr(p, meth)()) == tuple(float(x) for x in exp)

    # .coords (например, numpy/own type)
    if hasattr(p, "coords"):
        coords = getattr(p, "coords")
        if isinstance(coords, (tuple, list)) and len(coords) == 2:
            return tuple(float(x) for x in coords) == tuple(float(x) for x in exp)
        if hasattr(coords, "__getitem__") and len(coords) > 0:
            return tuple(float(x) for x in coords[0]) == tuple(float(x) for x in exp)

    # numpy array/прочие массивы
    try:
        t = tuple(float(x) for x in list(p))
        if len(t) == 2:
            return t == tuple(float(x) for x in exp)
    except Exception:
        pass

    raise TypeError(f"Неизвестный формат точки: {p} ({type(p)})")


@pytest.fixture
def sample_shapes(minimal_shape):
    # Возвращаем несколько shape'ов с разными полями
    shape1 = Shape(label="a", coords=[[1.0, 2.0], [3.0, 2.0], [3.0, 4.0], [1.0, 4.0]], type=minimal_shape.type)
    shape2 = Shape(label="b", coords=[[5.0, 6.0], [7.0, 6.0], [7.0, 8.0], [5.0, 8.0]], type=minimal_shape.type)
    shape3 = Shape(label="a", coords=[[9.0, 10.0], [11.0, 10.0], [11.0, 12.0], [9.0, 12.0]], type=minimal_shape.type, number=1, wz_number=3)
    return [shape1, shape2, shape3]


def test_set_shift_point_returns_new_list(sample_shapes):
    new_shapes = set_shift_point(sample_shapes, (1, 2))
    assert all(point_eq(s.shift_point, (1, 2)) for s in new_shapes)


def test_set_shift_point_filters_label(sample_shapes):
    result = set_shift_point(sample_shapes, (3, 4), label="a")
    for s in result:
        if s.label == "a":
            assert point_eq(s.shift_point, (3, 4))
        else:
            assert s.shift_point is None


def test_get_shapes_by_number(sample_shapes):
    filtered = get_shapes_by_number(sample_shapes, 1)
    assert all(getattr(s, "number", None) == 1 for s in filtered)
    assert len(filtered) == 1


def test_get_shapes_by_wz_number(sample_shapes):
    filtered = get_shapes_by_wz_number(sample_shapes, 3)
    assert all(getattr(s, "wz_number", None) == 3 for s in filtered)
    assert len(filtered) == 1
