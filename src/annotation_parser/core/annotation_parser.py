__all__ = ['AnnotationParser']

from typing import Tuple, Any, Optional

from ..adapters.base_adapter import AdapterType
from ..shape import Shape


class AnnotationParser:
    """
        Класс-парсер для файлов разметки: преобразует json-данные в кортеж фигур Shape.
    """

    @staticmethod
    def parse(json_data: Any, adapter: AdapterType, shift_point: Optional[Any] = None) -> Tuple[Shape, ...]:
        """
            Преобразует json-данные аннотаций в кортеж фигур через указанный адаптер.
            Args:
                json_data: Загруженный json-словарь/список аннотаций.
                adapter: Класс-адаптер (например, LabelMeAdapter), реализующий load.
                shift_point: Дополнительная информация для смещения точек (по необходимости).
            Returns:
                Кортеж фигур (Shape, ...).
            Raises:
                ValueError: Если адаптер не реализует load.
        """
        if not hasattr(adapter, "load"):
            raise ValueError(f"Adapter '{adapter.__name__}' does not implement 'load' method.")

        shapes = adapter.load(json_data, shift_point=shift_point)
        if not isinstance(shapes, (list, tuple)):
            raise ValueError(f"Adapter '{adapter.__name__}' returned unsupported type: {type(shapes)}")

        return tuple(shapes)
