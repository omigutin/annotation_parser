__all__ = ['LabelMeAdapter']

from typing import Optional, Tuple, Any

from ..shape import Shape
from ..types import ShiftPointType
from ..public_enums import ShapeType, ShapePosition
from ..models.labelme_model import JsonLabelmeShape, JsonLabelme
from .adapter_registration import AdapterRegistration
from .base_adapter import BaseAdapter


class LabelMeAdapter(BaseAdapter, metaclass=AdapterRegistration):
    """
        Адаптер для преобразования LabelMe-моделей в бизнес-объекты Shape.
        Контракт реализует load и shapes_to_json для bidirectional конверсии.
    """

    adapter_name = "labelme"

    @staticmethod
    def load(json_data: Any, shift_point: ShiftPointType = None) -> Tuple[Shape, ...]:
        """
            Преобразует LabelMe-JSON в кортеж Shape.
            Args:
                json_data (dict): LabelMe-данные.
                shift_point (ShiftPointType): Смещение координат (если требуется).
            Returns:
                Tuple[Shape, ...]: Кортеж фигур Shape.
            Raises:
                ValueError: Если структура json_data некорректна.
        """
        if not isinstance(json_data, dict) or "shapes" not in json_data:
            raise ValueError("LabelMe JSON должен содержать ключ 'shapes'")
        return tuple(LabelMeAdapter._to_shape(js, shift_point=shift_point) for js in json_data["shapes"])

    @staticmethod
    def shapes_to_json(original_json: Any, shapes: Tuple[Shape, ...]) -> dict:
        """
            Сериализует кортеж Shape обратно в json для сохранения LabelMe.
            Args:
                original_json: Исходный json для возможной передачи доп. полей.
                shapes: Кортеж Shape.
            Returns:
                dict: LabelMe-JSON c обновлённым shapes и всеми обязательными полями.
        """
        # Собираем shapes-модели по pydantic
        shapes_models = [LabelMeAdapter._shape_to_raw(shape) for shape in shapes]

        # Используем только реально существующие поля, иначе дефолты от pydantic
        fields = {}
        if original_json:
            for k in (
            "version", "flags", "imagePath", "imageData", "imageHeight", "imageWidth", "lineColor", "fillColor"):
                v = original_json.get(k, None)
                if v is not None:
                    fields[k] = v
        fields["shapes"] = shapes_models

        # Собираем объект по полной модели (дефолты модели будут использоваться если значения нет)
        labelme_obj = JsonLabelme(**fields)
        return labelme_obj.model_dump(mode='json', by_alias=True)

    @staticmethod
    def _to_shape(js: Any, shift_point: ShiftPointType = None) -> Shape:
        """
            Преобразует JsonLabelmeShape (pydantic) в Shape.
            Args:
                js: Модель фигуры LabelMe.
                shift_point: Опциональный Point для смещения.
            Returns:
                Shape: Бизнес-объект.
            """
        if not isinstance(js, JsonLabelmeShape):
            js = JsonLabelmeShape.model_validate(js)
        return Shape(
            label=BaseAdapter._get_field(js, "label"),
            coords=js.points,
            type=LabelMeAdapter._parse_shape_type(BaseAdapter._get_field(js, "shape_type")),
            number=BaseAdapter._get_field(js, "group_id"),
            description=BaseAdapter._get_field(js, "description"),
            flags=BaseAdapter._get_field(js, "flags", {}),
            mask=BaseAdapter._get_field(js, "mask"),
            position=LabelMeAdapter._parse_position(BaseAdapter._get_field(js, "position", None)),
            wz_number=BaseAdapter._get_field(js, "wz"),
            shift_point=shift_point,
            meta=getattr(js, "model_extra", {})
        )

    @staticmethod
    def _shape_to_raw(shape: Shape) -> JsonLabelmeShape:
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
    def _parse_position(val: Optional[str | ShapePosition]) -> Optional[ShapePosition]:
        if val is None:
            return None
        if isinstance(val, ShapePosition):
            return val
        if isinstance(val, str):
            try:
                return ShapePosition[val.upper()]
            except Exception:
                raise ValueError(f"Unknown ShapePosition: {val}")
        raise TypeError(f"Expected ShapePosition instance or str, got {type(val).__name__}")