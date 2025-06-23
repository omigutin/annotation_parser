__all__ = ['ShapeType', 'ShapePosition', 'Adapters']

from enum import Enum


class Adapters(Enum):
    """ Адаптеры регистрируем с доступом к .model """
    labelme = "labelme"
    coco = "coco"
    voc = "voc"


class ShapePosition(str, Enum):
    """ Положение фигуры относительно области интереса """
    LEFT = 'left'
    RIGHT = 'right'
    TOP = 'top'
    BOTTOM = 'bottom'
    CENTRE = 'centre'


class ShapeType(str, Enum):
    """ Типы фигур """
    LINE = 'line'
    POINT = 'point'
    POLYGON = 'polygon'
    RECTANGLE = 'rectangle'
