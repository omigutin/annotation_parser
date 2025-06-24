__all__ = ['AnnotationFile']

from typing import Tuple, Any, Optional, Union, Callable
from pathlib import Path
import json

from ..adapters.base_adapter import AdapterType
from ..public_enums import Adapters
from ..shape import Shape
from ..adapters.adapter_factory import AdapterFactory
from .annotation_parser import AnnotationParser
from .annotation_saver import AnnotationSaver
from ..types import ShiftPointType


class AnnotationFile:
    """
        Класс-хранилище для работы с файлами разметки:
        - хранит распарсенный json (если keep_json=True)
        - хранит кортеж фигур
        - умеет обновлять, сериализовать и сохранять
    """
    def __init__(self,
                 file_path: Union[str, Path],
                 markup_type: str | Adapters,
                 keep_json: bool = False,
                 validate_file: bool = True,
                 shift_point: ShiftPointType = None) -> None:
        """
            Инициализация объекта для работы с файлом разметки.
            Args:
                file_path (str | Path): Путь к файлу разметки.
                markup_type (str | Adapters): Тип формата разметки (например, 'labelme').
                keep_json (bool, optional): Если True — хранить исходный json в памяти (для ускорения и доп. операций).
                                            По умолчанию False.
                validate_file (bool, optional):
                    Проверять существование файла при инициализации.
                    - True (по умолчанию): используется для чтения/парсинга — файл должен существовать.
                    - False: используется для сценариев записи/сохранения по новому пути, когда файл может ещё
                             не существовать (например, при экспорте или копировании).
                shift_point (Any, optional): Смещение координат (если требуется по задаче).
            Raises:
                FileNotFoundError: Если validate_file=True и файл не найден.
                ValueError: Если не удалось создать адаптер для указанного типа разметки.
        """
        self._file_path: str = (self._get_file_path(file_path) if validate_file else str(Path(file_path)))
        self._adapter: AdapterType = AdapterFactory.get_adapter(markup_type)
        if keep_json and (validate_file or Path(file_path).exists()):
            self._json_data = self._load_json(self._file_path)
        else:
            self._json_data = None
        self._shapes: Optional[Tuple[Shape, ...]] = None
        self._shift_point: ShiftPointType = shift_point

    def parse(self) -> Tuple[Shape, ...]:
        """
            Парсит аннотационный файл и возвращает кортеж фигур Shape.
            - Использует ранее загруженный JSON из файла (self._json_data),
              так как объект всегда создаётся через create(..., keep_json=True).
            - Преобразует данные через адаптер в кортеж фигур.
            - Кэширует результат для повторных вызовов (self._shapes).
            Returns:
                Tuple[Shape, ...]: Кортеж фигур (Shape), извлечённых из файла разметки.
            Raises:
                ValueError: Если возникли ошибки при обработке структуры файла или адаптера.
        """
        if self._shapes is None:
            self._shapes = AnnotationParser.parse(self._json_data, self._adapter, shift_point=self._shift_point)
        return self._shapes

    def save(self, shapes: Tuple[Shape, ...], backup: bool = False) -> None:
        """
            Сохраняет фигуры в файл разметки, заменяя аннотационные данные.
            Если backup=True и файл существует, автоматически создаёт резервную копию с меткой времени.
            Args:
                shapes: Кортеж фигур для сохранения.
                backup: Делать ли резервную копию перед перезаписью (по умолчанию — НЕТ).
            Raises:
                FileNotFoundError, OSError, ValueError — если возникли ошибки при записи или доступе к файлу.
        """
        AnnotationSaver.save(shapes=shapes,
                             adapter=self._adapter,
                             file_path=self._file_path,
                             json_data=self._json_data,
                             backup=backup)

    @staticmethod
    def _load_json(file_path: str) -> Any:
        """
            Загружает JSON-файл.
            Args:
                file_path: Путь к файлу.
            Returns:
                Любой объект Python (dict или list), соответствующий JSON-структуре.
            Raises:
                FileNotFoundError: если файл не найден.
                json.JSONDecodeError: если файл некорректный JSON.
                OSError: если ошибка доступа к файлу.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"[ERROR] File not found: {file_path}")
            raise
        except json.JSONDecodeError as e:
            print(f"[ERROR] Invalid JSON in file {file_path}: {e}")
            raise
        except OSError as e:
            print(f"[ERROR] File access error for {file_path}: {e}")
            raise

    @staticmethod
    def _get_file_path(file_path: str | Path) -> str:
        """
            Проверяет существование файла разметки и возвращает его путь в виде строки.
            Args:
                file_path (str | Path): Путь к файлу разметки.
            Returns:
                str: Абсолютный путь к файлу.
            Raises:
                FileNotFoundError: Если файл по указанному пути не найден.
        """
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f'Файл разметки не найден: {file_path}')
        return str(path)
