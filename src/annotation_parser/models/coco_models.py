__all__ = ['JsonCocoAnnotation', 'JsonCoco']

from typing import Optional, Any, List, Dict, Union
from pydantic import BaseModel, ConfigDict, Field


class JsonCocoAnnotation(BaseModel):
    """
        Pydantic-модель для аннотации COCO.
        Args:
            id (int): Уникальный id аннотации.
            image_id (int): id изображения.
            category_id (int): id категории объекта.
            bbox (List[float]): [x, y, width, height] — ограничивающая рамка.
            segmentation (Optional[Union[List, Dict]]): Маска сегментации (любая структура).
            area (Optional[float]): Площадь объекта.
            iscrowd (Optional[int]): Признак “скопления” (1 — crowd, 0 — нет).
    """
    id: int
    image_id: int
    category_id: int
    bbox: List[float] = Field(..., description="[x, y, width, height]")
    segmentation: Optional[Union[List[Any], Dict[str, Any]]] = None
    area: Optional[float] = None
    iscrowd: Optional[int] = None

    model_config = ConfigDict(extra="allow")


class JsonCoco(BaseModel):
    """
        Pydantic-модель для файла аннотаций COCO.
        Args:
            images (List[dict]): Список описаний изображений.
            annotations (List[JsonCocoAnnotation]): Список аннотаций.
            categories (List[dict]): Список категорий объектов.
    """
    images: List[Dict[str, Any]]
    annotations: List[JsonCocoAnnotation]
    categories: List[Dict[str, Any]]

    model_config = ConfigDict(extra="allow")
