__all__ = ['JsonLabelmeShape', 'JsonLabelme']

from typing import Optional, Any, List
from pydantic import BaseModel, ConfigDict


class JsonLabelmeShape(BaseModel):
    """
        Pydantic-модель одной фигуры из LabelMe JSON.
        Позволяет хранить любые дополнительные (кастомные) поля через model_extra.
    """
    label: str
    points: list
    group_id: Optional[int] = None
    description: Optional[str] = None
    shape_type: str
    flags: dict = {}
    mask: Any = None

    model_config = ConfigDict(extra="allow")


class JsonLabelme(BaseModel):
    """ Pydantic-модель всего LabelMe JSON-файла. """
    version: str = "5.5.0"
    flags: dict = {}
    shapes: List[JsonLabelmeShape] = []
    imagePath: str = "cam.jpg"
    imageData: Optional[str] = None
    imageHeight: int = 1080
    imageWidth: int = 1920
    lineColor: tuple[int, int, int, int] = (0, 255, 0, 128)
    fillColor: tuple[int, int, int, int] = (255, 0, 0, 128)

    model_config = ConfigDict(extra="allow")
