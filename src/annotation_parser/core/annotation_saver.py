__all__ = ['AnnotationSaver']

import shutil
from datetime import datetime
import json
from pathlib import Path
from typing import Tuple, Any, Union

from ..adapters.base_adapter import AdapterType
from ..shape import Shape


class AnnotationSaver:
    """
        Класс-сохранятор для файлов разметки: преобразует кортеж фигур Shape и
        дополнительные данные в финальный JSON, записывает на диск.
        Требует, чтобы адаптер реализовывал метод shapes_to_json.
    """

    @staticmethod
    def save(
            shapes: Tuple[Shape, ...],
            adapter: AdapterType,
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
            AnnotationSaver._make_backup(file_path)
        new_json = adapter.shapes_to_json(json_data, shapes)
        AnnotationSaver._write_json_to_file(new_json, file_path)

    @staticmethod
    def _make_backup(path: Union[str, Path]) -> None:
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

    @staticmethod
    def _write_json_to_file(data: dict, file_path: str | Path) -> None:
        """
            Записывает словарь (json-объект) в файл в формате JSON.
            Args:
                data (dict): Данные для сохранения.
                file_path (str | Path): Куда писать.
            Raises:
                OSError: при ошибках доступа к файлу.
        """
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
