__all__ = ['VocAdapter']

from typing import Optional, Any, Tuple, Dict

from shapely.geometry import Point

from ..shape import Shape
from ..public_enums import ShapeType
from ..models.voc_models import JsonVocObject
from .adapter_registration import AdapterRegistration
from .base_adapter import BaseAdapter


class VocAdapter(BaseAdapter, metaclass=AdapterRegistration):
    """
        Адаптер для преобразования объектов PascalVOC в бизнес-объекты Shape.
        Реализует интерфейс BaseAdapter для bidirectional-конверсии разметки VOC.
    """

    adapter_name = "voc"

    @staticmethod
    def load(json_data: Any, shift_point: Optional[Point] = None) -> Tuple[Shape, ...]:
        """
            Преобразует VOC-аннотацию (dict с объектами) в кортеж Shape.
            Args:
                json_data (dict): Данные VOC (например, {"objects": [...]}).
                shift_point (Optional[Point]): Опциональное смещение координат.
            Returns:
                Tuple[Shape, ...]: Кортеж Shape.
            Raises:
                ValueError: Если структура данных не поддерживается.
        """
        # Здесь предполагается, что json_data["objects"] — это список объектов типа JsonVocObject или dict
        if not isinstance(json_data, dict) or "objects" not in json_data:
            raise ValueError("VOC JSON должен содержать ключ 'objects'")

        objects = json_data["objects"]
        result = []
        for obj in objects:
            # Если obj — dict, превращаем в модель
            if not isinstance(obj, JsonVocObject):
                obj = JsonVocObject.model_validate(obj)
            result.append(VocAdapter.to_shape(obj, shift_point=shift_point))
        return tuple(result)

    @staticmethod
    def to_shape(obj: JsonVocObject, shift_point: Optional[Point] = None) -> Shape:
        """
            Преобразует JsonVocObject в Shape.
            Args:
                obj (JsonVocObject): Объект VOC.
                shift_point (Optional[Point]): Смещение.
            Returns:
                Shape: Бизнес-объект.
        """
        shape_type = ShapeType.RECTANGLE
        coords = BaseAdapter._two_coords_to_four(
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

    @staticmethod
    def shapes_to_json(original_json: Any, shapes: Tuple[Shape, ...]) -> Dict:
        """
            Сериализует кортеж Shape обратно в VOC-структуру.
            Args:
                original_json: Оригинальный json для поддержки дополнительных полей.
                shapes: Кортеж Shape для сохранения.
            Returns:
                dict: VOC-JSON c обновлённым objects.
        """
        # Глубокое копирование оригинала, если он был
        import copy
        json_out = copy.deepcopy(original_json) if original_json else {}
        json_out["objects"] = [VocAdapter.shape_to_raw(shape).model_dump() for shape in shapes]
        return json_out

    @staticmethod
    def shape_to_raw(shape: Shape) -> JsonVocObject:
        """
            Преобразует Shape обратно в VOC-модель.
            Args:
                shape (Shape): Бизнес-объект.
            Returns:
                JsonVocObject: Модель VOC.
        """
        # Приводим координаты к 4 точкам в любом случае
        coords = BaseAdapter._two_coords_to_four(shape.coords, ShapeType.RECTANGLE)
        if not (isinstance(coords, (list, tuple)) and len(coords) == 4):
            raise ValueError("Некорректные координаты для VOC: должны быть 2 или 4 точки")
        xmin, ymin = coords[0]
        xmax, ymax = coords[2]
        return JsonVocObject(
            name=shape.label,
            bndbox_xmin=float(xmin),
            bndbox_ymin=float(ymin),
            bndbox_xmax=float(xmax),
            bndbox_ymax=float(ymax)
        )
