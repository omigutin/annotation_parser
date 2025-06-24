__all__ = ['to_point', 'to_coords', 'two_coords_to_four']

from shapely.geometry import Point
from typing import overload, Tuple, List, Any, Optional

from ..public_enums import ShapeType
from ..types import ShiftPointType, CoordsInput, Coords


@overload
def to_point(obj: None) -> None: ...
@overload
def to_point(obj: Point) -> Point: ...
@overload
def to_point(obj: Tuple[float, float]) -> Point: ...
@overload
def to_point(obj: List[float]) -> Point: ...
@overload
def to_point(obj: Any) -> ShiftPointType: ...


def to_point(obj: Any) -> ShiftPointType:
    """
        Преобразует вход к shapely.geometry.Point:
          - tuple, list → Point(x, y)
          - Point → Point
          - объект с .x и .y → Point
          - None → None
    """
    if obj is None:
        return None
    if isinstance(obj, Point):
        return obj
    if isinstance(obj, (list, tuple)) and len(obj) == 2:
        x, y = obj
        return Point(x, y)
    if hasattr(obj, 'x') and hasattr(obj, 'y'):
        return Point(obj.x, obj.y)
    raise TypeError(f"Cannot convert {type(obj)} to Point")


@overload
def to_coords(coords: None) -> None: ...
@overload
def to_coords(coords: CoordsInput) -> Optional[Coords]: ...


def to_coords(coords: Any) -> Optional[Coords]:
    """
        Преобразует любые итерируемые пары (int/float/str) в Coords (List[List[float]])
        Пример входа: [[1, 2], (3, 4), [5.1, 6.2]]
    """
    if coords is None:
        return None
    out = []
    for pair in coords:
        if not (isinstance(pair, (list, tuple)) and len(pair) == 2):
            raise ValueError(f"Each coordinate must be a pair of numbers, got: {pair}")
        x, y = pair
        out.append([float(x), float(y)])
    return out


def two_coords_to_four(coords: list, shape_type: str | ShapeType) -> list:
    """ Для прямоугольника: если передано 2 точки — строит 4 угла. """
    stype = shape_type.value if isinstance(shape_type, ShapeType) else shape_type
    if (stype.lower() == "rectangle" or stype == ShapeType.RECTANGLE) and len(coords) == 2:
        x1, y1 = coords[0]
        x2, y2 = coords[1]
        return [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]
    return coords
