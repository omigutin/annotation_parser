__all__ = ['ShiftPointType', 'Coords', 'CoordsInput']

from typing import List, Tuple, Union, Sequence, Any, Optional
from shapely.geometry import Point

# То, как можно передать shift_point
ShiftPointType = Optional[Union[Point, Tuple[float, float], List[float], Any]]

# Координаты: [[x, y], ...]
Coords = List[List[float]]
CoordPair = List[float]  # или Tuple[float, float], если хочешь

# Вход: все, что можно подать на coords
CoordsInput = Sequence[Union[List[Any], Tuple[Any, Any]]]
