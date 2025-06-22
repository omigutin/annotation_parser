from typing import Optional

from shapely.geometry import Point

from ..shape import Shape
from ..public_enums import ShapeType
from ..models.coco_models import JsonCocoAnnotation
from .base_adapter import BaseAdapter


class CocoAdapter(BaseAdapter):
    """
        Адаптер для преобразования аннотации COCO в Shape.
    """
    def to_shape(self, ann: JsonCocoAnnotation, shift_point: Optional[Point] = None) -> Shape:
        # Пример для COCO bbox: [x, y, width, height]
        shape_type = ShapeType.RECTANGLE
        bbox = ann.bbox
        coords = self._two_coords_to_four([[bbox[0], bbox[1]], [bbox[0] + bbox[2], bbox[1] + bbox[3]]], shape_type)
        return Shape(
            label=str(ann.category_id),
            coords=coords,
            type=shape_type,
            number=ann.id,
            description=None,
            flags=None,
            mask=None,
            position=None,
            wz_number=None,
            shift_point=shift_point,
            meta=getattr(ann, "model_extra", {})
        )
