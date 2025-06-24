__all__ = ['JsonVocObject', 'JsonVoc']

from typing import List, Optional, Any, Dict
from pydantic import BaseModel, ConfigDict, Field


class JsonVocObject(BaseModel):
    """
        Pydantic-модель для одного объекта (аннотации) в Pascal VOC.
        Args:
            name (str): Имя класса объекта.
            bndbox_xmin (float): Левая граница ограничивающего прямоугольника.
            bndbox_ymin (float): Верхняя граница ограничивающего прямоугольника.
            bndbox_xmax (float): Правая граница ограничивающего прямоугольника.
            bndbox_ymax (float): Нижняя граница ограничивающего прямоугольника.
    """
    name: str
    bndbox_xmin: float
    bndbox_ymin: float
    bndbox_xmax: float
    bndbox_ymax: float

    model_config = ConfigDict(extra="allow")


class JsonVoc(BaseModel):
    """
        Pydantic-модель для полного VOC-файла.
        Args:
            objects (List[JsonVocObject]): Список объектов.
            <...other standard VOC fields can be added as needed...>
    """
    objects: List[JsonVocObject] = Field(default_factory=list)
    # Дополнительные стандартные поля VOC можно добавить ниже:
    folder: Optional[str] = None
    filename: Optional[str] = None
    size: Optional[Dict[str, Any]] = None
    segmented: Optional[int] = None

    model_config = ConfigDict(extra="allow")
