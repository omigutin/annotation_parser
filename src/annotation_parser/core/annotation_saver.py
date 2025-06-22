__all__ = ['AnnotationSaver']

import shutil
from datetime import datetime
import json
from pathlib import Path
from typing import Tuple, Any, Union, Type

from ..adapters import BaseAdapter
from ..shape import Shape


class AnnotationSaver:
    """
        Класс-сохранятор для файлов разметки: преобразует кортеж фигур Shape и
        дополнительные данные в финальный JSON, записывает на диск.
    """

    @staticmethod
    def save(
            shapes: Tuple[Shape, ...],
            adapter: Type[BaseAdapter],
            file_path: Union[str, Path],
            json_data: Any,
            backup: bool = False) -> None:
        """
            Сохраняет кортеж фигур в файл разметки указанного формата.
            Args:
                shapes: Кортеж фигур Shape для сохранения.
                adapter: Строка или элемент Adapters, указывающий формат.
                file_path: Путь для сохранения файла.
                json_data: Оригинальный JSON (если есть, для поддержки дополнительных полей).
                backup: Делать ли резервную копию перед перезаписью (по умолчанию — да).
            Raises:
                NotImplementedError: Если адаптер не реализует метод shapes_to_json.
                ValueError: Если адаптер не найден.
        """
        if not hasattr(adapter, "shapes_to_json"):
            raise NotImplementedError(f"{adapter.__name__} must implement shapes_to_json()")

        if backup:
            AnnotationSaver.__make_backup(file_path)

        new_json = adapter.shapes_to_json(json_data, shapes)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(new_json, f, ensure_ascii=False, indent=2)

    @staticmethod
    def __make_backup(path: Union[str, Path]) -> None:
        """
            Создаёт резервную копию файла с добавлением временной метки к имени.
            Args:
                path: Путь к исходному файлу для резервирования.
            Raises:
                OSError: если не удалось скопировать файл.
        """
        orig_path = Path(path)
        if orig_path.exists():
            backup_path = orig_path.with_name(
                f"{orig_path.stem}_backup_{datetime.now():%Y%m%d_%H%M%S}{orig_path.suffix}")
            shutil.copy2(orig_path, backup_path)
