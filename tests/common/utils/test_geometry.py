import pytest
from shapely.geometry import Point

from annotation_parser.utils import to_point, to_coords, two_coords_to_four
from annotation_parser.public_enums import ShapeType


# --- to_point ---
@pytest.mark.parametrize("input_val,expected", [
    (None, None),
    (Point(1, 2), Point(1, 2)),
    ((3, 4), Point(3, 4)),
    ([5, 6], Point(5, 6)),
    (type("Dummy", (), {"x": 7, "y": 8})(), Point(7, 8)),
])
def test_to_point_good(input_val, expected):
    result = to_point(input_val)
    if result is None:
        assert expected is None
    else:
        assert isinstance(result, Point)
        assert (result.x, result.y) == (expected.x, expected.y)


def test_to_point_bad():
    with pytest.raises(TypeError):
        to_point("not a point")
    with pytest.raises(TypeError):
        to_point([1])  # Недостаточно координат


# --- to_coords ---
@pytest.mark.parametrize("coords,expected", [
    ([[1, 2], [3.0, 4]], [[1.0, 2.0], [3.0, 4.0]]),
    (([5, 6], [7, 8]), [[5.0, 6.0], [7.0, 8.0]]),
    ([(1.2, 3.4), (5.6, 7.8)], [[1.2, 3.4], [5.6, 7.8]]),
    (None, None),
])
def test_to_coords_good(coords, expected):
    assert to_coords(coords) == expected


def test_to_coords_invalid():
    with pytest.raises(ValueError):
        to_coords([[1, 2, 3], [4, 5]])  # not pairs


# --- two_coords_to_four ---
@pytest.mark.parametrize("coords,stype,expected", [
    ([[1, 2], [3, 4]], ShapeType.RECTANGLE, [[1, 2], [3, 2], [3, 4], [1, 4]]),
    ([[5, 6], [7, 8]], "rectangle", [[5, 6], [7, 6], [7, 8], [5, 8]]),
    ([[1, 2], [3, 4], [5, 6]], ShapeType.RECTANGLE, [[1, 2], [3, 4], [5, 6]]),
    ([[1, 2], [3, 4]], ShapeType.POLYGON, [[1, 2], [3, 4]]),
])
def test_two_coords_to_four(coords, stype, expected):
    assert two_coords_to_four(coords, stype) == expected
