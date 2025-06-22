from typing import Optional

from shapely.geometry import Point

from ..shape import Shape
from ..public_enums import ShapeType
from ..models.voc_models import JsonVocObject
from .base_adapter import BaseAdapter


class VocAdapter(BaseAdapter):
    """
        Адаптер для преобразования объекта PascalVOC в Shape.
    """
    def to_shape(self, obj: JsonVocObject, shift_point: Optional[Point] = None) -> Shape:
        shape_type = ShapeType.RECTANGLE
        coords = self._two_coords_to_four(
            [[obj.bndbox_xmin, obj.bndbox_ymin], [obj.bndbox_xmax, obj.bndbox_ymax]],
            shape_type
        )
        return Shape(
            label=obj.name,
            coords=coords,
            type=shape_type,
            number=None,
            description=None,
            flags=None,
            mask=None,
            position=None,
            wz_number=None,
            shift_point=shift_point,
            meta=getattr(obj, "model_extra", {})
        )
