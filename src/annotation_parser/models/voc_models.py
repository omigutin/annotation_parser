from typing import Optional
from pydantic import BaseModel, ConfigDict


class JsonVocObject(BaseModel):
    name: str
    bndbox_xmin: float
    bndbox_ymin: float
    bndbox_xmax: float
    bndbox_ymax: float
    model_config = ConfigDict(extra="allow")


class JsonVoc(BaseModel):
    objects: list[JsonVocObject]
    # ... другие стандартные поля VOC ...
    model_config = ConfigDict(extra="allow")
