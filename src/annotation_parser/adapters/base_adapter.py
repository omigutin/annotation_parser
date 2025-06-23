__all__ = ['BaseAdapter', 'AdapterType']

from abc import ABC, abstractmethod
from typing import Any, Optional, Tuple, Dict, TypeVar, Generic

from ..shape import Shape
from ..public_enums import ShapeType

AdapterType = TypeVar('AdapterType', bound='BaseAdapter')


class BaseAdapter(ABC, Generic[AdapterType]):
    """
        Абстрактный базовый класс для всех адаптеров форматов разметки.
        Контракт:
            - load: превращает json-данные в кортеж Shape.
            - shapes_to_json: сериализует кортеж Shape обратно в json (для сохранения).
        Для регистрации адаптеров используется AdapterFactory.
    """

    adapter_name: str = ""

    @staticmethod
    @abstractmethod
    def load(json_data: Any, shift_point: Optional[Any] = None) -> Tuple[Shape, ...]:
        """
            Преобразует json-данные в кортеж Shape.
            Args:
                json_data: Входные данные (dict или list).
                shift_point: Точка смещения для фигур (если требуется).
            Returns:
                Tuple[Shape, ...]: Кортеж бизнес-объектов Shape.
            """
        pass

    @staticmethod
    @abstractmethod
    def shapes_to_json(original_json: Any, shapes: Tuple[Shape, ...]) -> Dict:
        """
            Сериализует кортеж Shape обратно в json-структуру для сохранения.
            Args:
                original_json: Оригинальный json-файл разметки (может быть нужен для обновления полей).
                shapes: Кортеж Shape для сохранения.
            Returns:
                dict: Сериализованный json-объект.
        """
        pass

    @staticmethod
    def _two_coords_to_four(coords: list, shape_type: str | ShapeType) -> list:
        """ Для прямоугольника: если передано 2 точки — строит 4 угла. """
        stype = shape_type.value if isinstance(shape_type, ShapeType) else shape_type
        if (stype.lower() == "rectangle" or stype == ShapeType.RECTANGLE) and len(coords) == 2:
            x1, y1 = coords[0]
            x2, y2 = coords[1]
            return [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]
        return coords

    @staticmethod
    def _get_field(obj: Any, name: str, default: Any = None) -> Any:
        """
            Универсально извлекает значение поля:
            - Сначала ищет среди атрибутов объекта (Pydantic-модель).
            - Затем в model_extra (для кастомных полей, если это Pydantic v2).
            - Если не найдено — возвращает default.
            Args:
                obj: Исходный объект (обычно Pydantic-модель).
                name: Имя поля.
                default: Значение по умолчанию, если поле не найдено.
            Returns:
                Значение поля или default.
        """
        value = getattr(obj, name, None)
        if value is not None:
            return value
        if hasattr(obj, "model_extra") and obj.model_extra:
            return obj.model_extra.get(name, default)
        return default
