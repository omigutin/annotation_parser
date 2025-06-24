from __future__ import annotations

__all__ = ['Shape']

from dataclasses import dataclass, field
from typing import Optional, Any, Dict, Tuple, List, Callable
import numpy as np
from shapely.geometry import LineString as Line, Polygon, Point

from .public_enums import ShapeType, ShapePosition
from .types import Coords
from .utils import to_point, to_coords, two_coords_to_four


@dataclass(frozen=True, slots=True)
class Shape:
    """
        Универсальный бизнес-объект для работы с фигурами разметки (полигон, линия, точка и др).

        Основные возможности:
            - Унифицированное представление любой фигуры из разметки (LabelMe, COCO, VOC и др.).
            - Быстрый доступ к ключевым геометрическим свойствам: контур, bounding box, линия и др.
            - Поддержка смещения (shift_point) для расчёта относительных координат.
            - Расширяемость через meta (можно хранить любые дополнительные атрибуты).

        Args:
            label (str): Метка фигуры (например, 'person', 'car').
            coords (Coords): Список координат [[x, y], ...], определяющих фигуру.
            type (ShapeType): Тип фигуры (line, polygon, rectangle, point).
            number (Optional[int]): Номер или идентификатор фигуры (если есть).
            description (Optional[str]): Описание фигуры.
            flags (Optional[Dict]): Произвольные флаги, экспортируемые из разметки.
            mask (Optional[np.ndarray]): Маска сегментации (если присутствует).
            position (Optional[ShapePosition]): Положение фигуры (см. ShapePosition).
            wz_number (Optional[int]): Номер рабочей зоны (если разметка по зонам).
            shift_point (Optional[Point]): Точка смещения для относительных координат (shapely.geometry.Point и др.).
            meta (Dict): Любые дополнительные свойства (confidence, score, custom data и др.).
    """

    label: str
    coords: Coords
    type: ShapeType
    number: Optional[int] = None
    description: Optional[str] = None
    flags: Optional[Dict[str, Any]] = None
    mask: Optional[np.ndarray] = None
    position: Optional[ShapePosition] = None
    wz_number: Optional[int] = None
    shift_point: Optional[Point] = None
    meta: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """
            Приводит поля к внутреннему формату и гарантирует корректность структуры Shape.
              - shift_point всегда приводится к Point (или None).
              - coords всегда приводится к List[List[float]], числа приводятся к float.
              - Для прямоугольника с двумя точками coords автоматически преобразуются в четыре угла.
            Raises:
                ValueError: coords не могут быть преобразованы в корректную фигуру.
                TypeError: shift_point передан в неподдерживаемом формате.
        """
        object.__setattr__(self, 'shift_point', to_point(self.shift_point))
        norm_coords = to_coords(self.coords)
        norm_coords = two_coords_to_four(norm_coords, self.type)
        object.__setattr__(self, 'coords', norm_coords)

    @property
    def is_individual(self) -> bool:
        """ True, если фигура относится к определённой зоне (индивидуальная), иначе общая. """
        return self.number is not None

    @property
    def contour(self) -> np.ndarray:
        """ Контур (np.ndarray) из coords, shape (N, 1, 2) для OpenCV. """
        return np.array(self.coords, dtype=np.float32).reshape((-1, 1, 2))

    @property
    def rect(self) -> Tuple[float, float, float, float]:
        """ Ограничивающий прямоугольник (bounding box). """
        if not self.coords:
            raise ValueError("Shape.coords is empty, cannot compute bounds")
        poly = Polygon(self.coords)
        return poly.bounds

    @property
    def line(self) -> Line:
        """ shapely.geometry.LineString по coords. """
        return Line(self.coords)

    @property
    def shifted_coords(self) -> Coords:
        """
            Смещённые координаты (если shift_point задан).
            Supports nested coords (recursively).
        """
        if self.shift_point:
            def shift_pair(pair):
                # [x, y], любые числа (int, float, str)
                return [float(pair[0]) - self.shift_point.x, float(pair[1]) - self.shift_point.y]
            # Вложенные списки пока не поддерживаем, но можно рекурсивно
            # Если надо, напиши -- добавим рекурсию для многомерных случаев
            return [shift_pair(pair) for pair in self.coords]
        return self.coords

    @property
    def shifted_contour(self) -> np.ndarray:
        """ Контур по смещённым координатам. """
        return np.array(self.shifted_coords, dtype=np.float32).reshape((-1, 1, 2))

    @property
    def shifted_rect(self) -> Tuple[float, float, float, float]:
        """ Bounding box по смещённым координатам. """
        if not self.shifted_coords:
            raise ValueError("Shape.shifted_coords is empty, cannot compute bounds")
        poly = Polygon(self.shifted_coords)
        return poly.bounds

    @property
    def shifted_line(self) -> Line:
        """ shapely.geometry.LineString по смещённым координатам. """
        return Line(self.shifted_coords)

    def get(self, name: str, default: Any = None) -> Any:
        """ Универсальный getter: сначала стандартный атрибут, затем meta. """
        if hasattr(self, name):
            return getattr(self, name)
        if self.meta and name in self.meta:
            return self.meta[name]
        return default

    @staticmethod
    def set_shift_point(
            shapes: List["Shape"],
            shift_point: Any,
            *,
            label: Optional[str] = None,
            wz_number: Optional[int] = None,
            number: Optional[int] = None,
            filter_fn: Optional[Callable[["Shape"], bool]] = None) -> List["Shape"]:
        """
            Возвращает новый список фигур с установленным shift_point.
            Исходные фигуры не изменяются (иммутабельность).
            Можно фильтровать по label, wz_number, number, а также с помощью произвольной функции.
            Args:
                shapes: Список фигур (Shape).
                shift_point: Новая точка смещения (любого поддерживаемого формата).
                label: (опц.) Фильтр по label.
                wz_number: (опц.) Фильтр по номеру рабочей зоны.
                number: (опц.) Фильтр по number (группе).
                filter_fn: (опц.) Любая функция-фильтр (Shape -> bool).
            Returns:
                List[Shape]: Новый список фигур с обновлённым shift_point.
        """
        point = to_point(shift_point)

        def match(shape):
            if label is not None and shape.label != label:
                return False
            if wz_number is not None and shape.wz_number != wz_number:
                return False
            if number is not None and shape.number != number:
                return False
            if filter_fn and not filter_fn(shape):
                return False
            return True

        return [
            shape if not match(shape) else
            Shape(
                label=shape.label,
                coords=shape.coords,
                type=shape.type,
                number=shape.number,
                description=shape.description,
                flags=shape.flags,
                mask=shape.mask,
                position=shape.position,
                wz_number=shape.wz_number,
                shift_point=point,
                meta=shape.meta.copy()
            )
            for shape in shapes
        ]

    def __repr__(self) -> str:
        """ Краткое строковое представление для дебага. """
        return (
            f"Shape(label={self.label!r}, type={self.type!r}, "
            f"coords={self.coords!r}, number={self.number!r})"
        )
