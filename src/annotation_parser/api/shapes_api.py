"""
    High-Level Shape Operations API
    ==============================

    Functions for advanced operations on Shape objects.

    This module provides utilities to:
        - Filter shapes by label, number, or working zone number (wz_number)
        - Set (batch) shift_point for multiple shapes, with flexible filtering by label, number, wz_number, or custom filter

    Usage examples:
        new_shapes = set_shift_point(shapes, (100, 200), label='person')
        persons = get_shapes_by_label(shapes, 'person')
        specific = get_shapes_by_number(shapes, 5)
        wz_shapes = get_shapes_by_wz_number(shapes, 3)
"""


__all__ = [
    'set_shift_point',
    'get_shapes_by_label',
    'get_shapes_by_number',
    'get_shapes_by_wz_number',
    'filter_shapes',
]

from typing import Any, Optional, Tuple, List, Callable

from ..shape import Shape


def set_shift_point(
        shapes: List[Shape],
        shift_point: Any,
        *,
        label: Optional[str] = None,
        wz_number: Optional[int] = None,
        number: Optional[int] = None,
        filter_fn: Optional[Callable[[Shape], bool]] = None) -> List[Shape]:
    """
        Интерфейсная функция: возвращает новый список фигур с установленным shift_point.
        Исходные фигуры не изменяются (иммутабельность).
        Можно фильтровать фигуры по label, wz_number, number или произвольной функцией filter_fn.
        Args:
            shapes: Список фигур (Shape).
            shift_point: Новая точка смещения (Point, tuple, list, объект с .x/.y, ...).
            label: (опц.) Фильтр по label.
            wz_number: (опц.) Фильтр по номеру рабочей зоны.
            number: (опц.) Фильтр по number (группе).
            filter_fn: (опц.) Пользовательский фильтр: функция от Shape -> bool.
        Returns:
            List[Shape]: Новый список фигур с обновлённым shift_point.
    """
    return Shape.set_shift_point(
        shapes,
        shift_point,
        label=label,
        wz_number=wz_number,
        number=number,
        filter_fn=filter_fn,
    )


def get_shapes_by_label(
        shapes: Tuple[Shape, ...],
        label: str,
        individual: bool = True,
        common: bool = True) -> Tuple[Shape, ...]:
    """
        Фильтрует кортеж фигур по label и признакам индивидуальности.
        Args:
            shapes: Кортеж Shape для фильтрации.
            label: Искомый label.
            individual: Включать индивидуальные фигуры (с number).
            common: Включать общие фигуры (без number).
        Returns:
            Tuple[Shape, ...]: Отфильтрованный кортеж фигур.
    """
    if not individual and not common:
        return ()
    return tuple(
        shape for shape in shapes
        if shape.label == label and ((individual and shape.is_individual) or (common and not shape.is_individual))
    )


def get_shapes_by_number(
        shapes: Tuple[Shape, ...],
        number: Optional[int],
        individual: bool = True,
        common: bool = True) -> Tuple[Shape, ...]:
    """
        Фильтрует кортеж фигур по значению number (индивидуальный номер), с поддержкой индивидуальных и общих фигур.
        Args:
            shapes: Кортеж Shape для фильтрации.
            number: Искомый номер (number).
            individual: Включать индивидуальные фигуры (number совпадает).
            common: Включать общие фигуры (number=None).
        Returns:
            Tuple[Shape, ...]: Отфильтрованный кортеж фигур.
    """
    if not individual and not common:
        return ()
    return tuple(
        shape for shape in shapes
        if shape.number == number and ((individual and shape.is_individual) or (common and not shape.is_individual))
    )


def get_shapes_by_wz_number(
        shapes: Tuple[Shape, ...],
        wz_number: Optional[int],
        individual: bool = True,
        common: bool = True) -> Tuple[Shape, ...]:
    """
        Фильтрует кортеж фигур по номеру рабочей зоны (wz_number), с поддержкой индивидуальных и общих фигур.
        Args:
            shapes: Кортеж Shape для фильтрации.
            wz_number: Искомый номер рабочей зоны (wz_number).
            individual: Включать индивидуальные фигуры (wz_number совпадает).
            common: Включать общие фигуры (wz_number=None).
        Returns:
            Tuple[Shape, ...]: Отфильтрованный кортеж фигур.
    """
    if not individual and not common:
        return ()
    return tuple(
        shape for shape in shapes
        if shape.wz_number == wz_number and ((individual and shape.is_individual) or (common and not shape.is_individual))
    )


def filter_shapes(
            shapes: Tuple[Shape, ...],
            predicate: Callable[[Shape], bool],
            individual: bool = True,
            common: bool = True) -> Tuple[Shape, ...]:
    """
        Возвращает кортеж фигур, удовлетворяющих произвольному предикату и фильтрам individual/common.
        Args:
            shapes: Кортеж фигур (Shape).
            predicate: функция-условие от Shape -> bool.
            individual: Включать индивидуальные фигуры (по number).
            common: Включать общие фигуры (без number).
        Returns:
            Tuple[Shape, ...]: Кортеж фигур, удовлетворяющих предикату и фильтрам.
    """
    if not individual and not common:
        return ()
    return tuple(
        shape for shape in shapes
        if predicate(shape) and ((individual and shape.is_individual) or (common and not shape.is_individual))
    )
