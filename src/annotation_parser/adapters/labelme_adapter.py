from typing import Optional, Tuple, Any
from shapely.geometry import Point
from copy import deepcopy

from ..shape import Shape
from ..public_enums import ShapeType, ShapePosition
from ..models.labelme_models import JsonLabelmeShape, JsonLabelme
from .base_adapter import BaseAdapter


class LabelMeAdapter(BaseAdapter):
    """
        Адаптер для преобразования LabelMe-моделей в бизнес-объекты Shape.
        Контракт реализует from_json и shapes_to_json для bidirectional конверсии.
    """

    @staticmethod
    def from_json(json_data: Any, shift_point: Optional[Point] = None) -> Tuple[Shape, ...]:
        """
            Преобразует LabelMe-JSON в кортеж Shape.
            Args:
                json_data: dict — данные из файла LabelMe.
                shift_point: Point, если требуется смещение.
            Returns:
                Tuple[Shape, ...]: Кортеж фигур Shape.
            """
        if not isinstance(json_data, dict) or "shapes" not in json_data:
            raise ValueError("LabelMe JSON должен содержать ключ 'shapes'")
        return tuple(LabelMeAdapter.to_shape(js, shift_point=shift_point)
                     for js in json_data["shapes"])

    @staticmethod
    def to_shape(js: JsonLabelmeShape, shift_point: Optional[Point] = None) -> Shape:
        """
            Преобразует JsonLabelmeShape (pydantic) в Shape.
            Args:
                js: Модель фигуры LabelMe.
                shift_point: Опциональный Point для смещения.
            Returns:
                Shape: Бизнес-объект.
            """
        coords = BaseAdapter._two_coords_to_four(js.points, BaseAdapter._get_field(js, "shape_type"))
        label = BaseAdapter._get_field(js, "label")
        group_id = BaseAdapter._get_field(js, "group_id")
        description = BaseAdapter._get_field(js, "description")
        flags = BaseAdapter._get_field(js, "flags", {})
        mask = BaseAdapter._get_field(js, "mask")
        wz_number = BaseAdapter._get_field(js, "wz")
        position_val = BaseAdapter._get_field(js, "position")
        position = LabelMeAdapter._parse_position(position_val) if position_val else None
        shape_type = LabelMeAdapter._parse_shape_type(BaseAdapter._get_field(js, "shape_type"))

        return Shape(
            label=label,
            coords=coords,
            type=shape_type,
            number=group_id,
            description=description,
            flags=flags,
            mask=mask,
            position=position,
            wz_number=wz_number,
            shift_point=shift_point,
            meta=getattr(js, "model_extra", {})
        )

    @staticmethod
    def shapes_to_json(original_json: Any, shapes: Tuple[Shape, ...]) -> dict:
        """
            Сериализует кортеж Shape обратно в json для сохранения LabelMe.
            Args:
                original_json: Исходный json для возможной передачи доп. полей.
                shapes: Кортеж Shape.
            Returns:
                dict: LabelMe-JSON c обновлённым shapes.
            """
        json_out = deepcopy(original_json) if original_json else {}
        json_out["shapes"] = [LabelMeAdapter.shape_to_raw(shape).model_dump() for shape in shapes]
        return json_out

    @staticmethod
    def shape_to_raw(shape: Shape) -> JsonLabelmeShape:
        """
            Конвертирует бизнес-Shape обратно в pydantic-модель LabelMe.
            Args:
                shape: Объект Shape.
            Returns:
                JsonLabelmeShape.
            """
        return JsonLabelmeShape(
            label=shape.label,
            points=shape.coords,
            group_id=shape.number,
            description=shape.description,
            shape_type=shape.type.value if hasattr(shape.type, 'value') else str(shape.type),
            flags=shape.flags or {},
            mask=shape.mask
        )

    @staticmethod
    def _parse_shape_type(val: str | ShapeType) -> ShapeType:
        if isinstance(val, ShapeType):
            return val
        if isinstance(val, str):
            try:
                return ShapeType[val.upper()]
            except Exception:
                raise ValueError(f"Unknown ShapeType: {val}")
        raise TypeError(f"Expected ShapeType instance or str, got {type(val).__name__}")

    @staticmethod
    def _parse_position(val: str | ShapePosition) -> ShapePosition:
        if isinstance(val, ShapePosition):
            return val
        if isinstance(val, str):
            try:
                return ShapePosition[val.upper()]
            except Exception:
                raise ValueError(f"Unknown ShapePosition: {val}")
        raise TypeError(f"Expected ShapePosition instance or str, got {type(val).__name__}")