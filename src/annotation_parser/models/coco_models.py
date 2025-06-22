from typing import Optional, Any, List
from pydantic import BaseModel, ConfigDict


class JsonCocoAnnotation(BaseModel):
    id: int
    image_id: int
    category_id: int
    bbox: list  # [x, y, width, height]
    segmentation: Optional[Any] = None
    area: Optional[float] = None
    iscrowd: Optional[int] = None
    model_config = ConfigDict(extra="allow")


class JsonCoco(BaseModel):
    images: list
    annotations: List[JsonCocoAnnotation]
    categories: list
    model_config = ConfigDict(extra="allow")
