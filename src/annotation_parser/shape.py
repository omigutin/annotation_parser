__all__ = ['Shape']

from dataclasses import dataclass, field
from typing import Optional, Any, List, Dict, Tuple
import numpy as np
from shapely.geometry import Point, LineString as Line, Polygon

from .public_enums import ShapeType, ShapePosition

# Тип для координат: список пар [x, y]
Coords = List[List[float]]


@dataclass(frozen=True, slots=True)
class Shape:
    """
        Универсальный бизнес-объект для работы с фигурами разметки (полигон, линия, точка и др).

        Основные возможности:
            - Унифицированное представление любой фигуры из разметки (LabelMe, COCO, VOC и др.).
            - Быстрый доступ к ключевым геометрическим свойствам: контур, bounding box, линия и др.
            - Поддержка смещения (shift_point) для расчёта относительных координат.
            - Расширяемость через meta (можно хранить любые дополнительные атрибуты).

        Samples:
            for shape in shapes:
                print(shape.label, shape.type, shape.rect)
                img = cv2.polylines(img, [shape.contour], ...)

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
            shift_point (Optional[Point]): Точка смещения для относительных координат (shapely.geometry.Point).
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

    @property
    def is_individual(self) -> bool:
        """
            Возвращает True, если фигура относится к определённой зоне (индивидуальная),
            и False — если она общая (относится ко всем зонам, number=None).
        """
        return self.number is not None

    @property
    def contour(self) -> np.ndarray:
        """
            Контур (np.ndarray) из coords.
            Returns:
                np.ndarray: Контур для OpenCV или вычислений, shape (N, 1, 2).
        """
        return np.array(self.coords, dtype=np.float32).reshape((-1, 1, 2))

    @property
    def rect(self) -> Tuple[float, float, float, float]:
        """
            Ограничивающий прямоугольник (bounding box) для фигуры.
            Returns:
                (minx, miny, maxx, maxy) как tuple из float.
            Raises:
                ValueError: Если coords пусты.
        """
        if not self.coords:
            raise ValueError("Shape.coords is empty, cannot compute bounds")
        poly = Polygon(self.coords)
        return poly.bounds

    @property
    def line(self) -> Line:
        """
            Линия (shapely.geometry.LineString) по coords.
            Returns:
                Line: Линия по всем точкам coords.
        """
        return Line(self.coords)

    @property
    def shifted_coords(self) -> Coords:
        """
            Смещённые координаты (если shift_point задан).
            Returns:
                Coords: Список координат, сдвинутых относительно shift_point.
        """
        if self.shift_point:
            return [[x - self.shift_point.x, y - self.shift_point.y] for x, y in self.coords]
        return self.coords

    @property
    def shifted_contour(self) -> np.ndarray:
        """
            Контур (np.ndarray) из смещённых координат.
            Returns:
                np.ndarray: Контур для OpenCV по смещённым coords, shape (N, 1, 2).
        """
        return np.array(self.shifted_coords, dtype=np.float32).reshape((-1, 1, 2))

    @property
    def shifted_rect(self) -> Tuple[float, float, float, float]:
        """
            Ограничивающий прямоугольник по смещённым координатам.
            Returns:
                (minx, miny, maxx, maxy) как tuple из float.
            Raises:
                ValueError: Если coords пусты.
        """
        if not self.shifted_coords:
            raise ValueError("Shape.shifted_coords is empty, cannot compute bounds")
        poly = Polygon(self.shifted_coords)
        return poly.bounds

    @property
    def shifted_line(self) -> Line:
        """
            Линия (shapely.geometry.LineString) по смещённым координатам.
            Returns:
                Line: Линия по всем смещённым точкам.
        """
        return Line(self.shifted_coords)

    def get(self, name: str, default: Any = None) -> Any:
        """
            Универсальный getter: ищет имя сначала среди стандартных атрибутов, затем в meta.
            Args:
                name (str): Имя атрибута или ключа meta.
                default: Значение по умолчанию, если не найдено.
            Returns:
                Любое найденное значение, иначе default.
        """
        if hasattr(self, name):
            return getattr(self, name)
        if self.meta and name in self.meta:
            return self.meta[name]
        return default

    def __repr__(self) -> str:
        """ Краткое строковое представление для дебага. """
        return (
            f"Shape(label={self.label!r}, type={self.type!r}, "
            f"coords={self.coords!r}, number={self.number!r})"
        )
