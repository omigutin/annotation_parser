__all__ = ['CocoAdapter']

from typing import Optional, Any, Tuple, Dict
from shapely.geometry import Point

from ..shape import Shape
from ..public_enums import ShapeType
from ..models import JsonCocoAnnotation
from .adapter_registration import AdapterRegistration
from .base_adapter import BaseAdapter


class CocoAdapter(BaseAdapter, metaclass=AdapterRegistration):
    """
        Адаптер для преобразования объектов COCO в бизнес-объекты Shape.
        Реализует интерфейс BaseAdapter для bidirectional-конверсии разметки COCO.
    """

    adapter_name = "coco"

    @staticmethod
    def load(json_data: Any, shift_point: Optional[Point] = None) -> Tuple[Shape, ...]:
        """
            Преобразует COCO-аннотации (dict с annotations и categories) в кортеж Shape.
            Args:
                json_data (dict): Данные COCO ({"annotations": [...], "categories": [...], ...}).
                shift_point (Optional[Point]): Смещение.
            Returns:
                Tuple[Shape, ...]: Кортеж Shape.
            Raises:
                ValueError: Если структура данных не поддерживается.
        """
        if not isinstance(json_data, dict) or "annotations" not in json_data:
            raise ValueError("COCO JSON должен содержать ключ 'annotations'")
        # Маппинг категорий (id -> name)
        category_map = {cat['id']: cat['name'] for cat in json_data.get("categories", [])}
        result = []
        for ann in json_data["annotations"]:
            if not isinstance(ann, JsonCocoAnnotation):
                ann = JsonCocoAnnotation.model_validate(ann)
            label = category_map.get(ann.category_id, str(ann.category_id))
            result.append(CocoAdapter.to_shape(ann, label, shift_point))
        return tuple(result)

    @staticmethod
    def to_shape(obj: JsonCocoAnnotation, label: str, shift_point: Optional[Point] = None) -> Shape:
        """
            Преобразует JsonCocoAnnotation в Shape.
            Args:
                obj (JsonCocoAnnotation): Аннотация COCO.
                label (str): Название категории.
                shift_point (Optional[Point]): Смещение.
            Returns:
                Shape: Бизнес-объект.
        """
        # COCO bbox: [x, y, width, height]
        x, y, w, h = obj.bbox
        coords = BaseAdapter._two_coords_to_four([[x, y], [x + w, y + h]], ShapeType.RECTANGLE)
        return Shape(
            label=label,
            coords=coords,
            type=ShapeType.RECTANGLE,
            number=obj.id,
            description=None,
            flags={},
            mask=None,
            position=None,
            wz_number=None,
            shift_point=shift_point,
            meta=getattr(obj, "model_extra", {})
        )

    @staticmethod
    def shapes_to_json(original_json: Any, shapes: Tuple[Shape, ...]) -> Dict:
        """
            Сериализует кортеж Shape обратно в COCO-структуру.
            Args:
                original_json: Оригинальный json (сохраняет все поля кроме "annotations").
                shapes: Кортеж Shape.
            Returns:
                dict: COCO-JSON c обновлённым "annotations".
        """
        import copy
        json_out = copy.deepcopy(original_json) if original_json else {}
        json_out["annotations"] = [CocoAdapter.shape_to_raw(shape).model_dump() for shape in shapes]
        return json_out

    @staticmethod
    def shape_to_raw(shape: Shape) -> JsonCocoAnnotation:
        """
            Преобразует Shape обратно в COCO-аннотацию.
            Args:
                shape (Shape): Бизнес-объект.
            Returns:
                JsonCocoAnnotation: Модель COCO.
        """
        coords = BaseAdapter._two_coords_to_four(shape.coords, ShapeType.RECTANGLE)
        x1, y1 = coords[0]
        x2, y2 = coords[2]
        bbox = [float(x1), float(y1), float(x2 - x1), float(y2 - y1)]
        # Сюда можно добавить category_id если есть маппинг label -> id
        return JsonCocoAnnotation(
            id=int(shape.number) if shape.number is not None else None,
            image_id=None,
            category_id=None,  # нужно прокидывать, если есть маппинг label->id
            bbox=bbox,
            segmentation=None,
            area=None,
            iscrowd=None
        )
