import os
import json
import tempfile
from pathlib import Path

import pytest
from annotation_parser.core.annotation_saver import AnnotationSaver
from annotation_parser.shape import Shape


# ----- Мок-адаптер -----
class DummyAdapter:
    @staticmethod
    def shapes_to_json(original_json, shapes):
        # Просто сохраняет все атрибуты shape в json
        return {
            "shapes": [
                {
                    "label": shape.label,
                    "coords": shape.coords,
                    "type": str(shape.type),
                }
                for shape in shapes
            ]
        }


def make_shape():
    return Shape(label="person", coords=[[0, 0], [1, 1]], type="line")


@pytest.fixture
def tmp_json_file(tmp_path):
    file_path = tmp_path / "out.json"
    file_path.write_text('{}', encoding='utf-8')
    return file_path


def test_saves_file(tmp_path):
    file_path = tmp_path / "file.json"
    shape = make_shape()
    # Файл ещё не существует, не будет backup
    AnnotationSaver.save((shape,), DummyAdapter, file_path, json_data=None, backup=False)
    # Проверяем файл
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["shapes"][0]["label"] == "person"
    assert data["shapes"][0]["coords"] == [[0.0, 0.0], [1.0, 1.0]]


def test_backup_is_created(tmp_path):
    file_path = tmp_path / "backup_me.json"
    file_path.write_text('{"shapes": []}', encoding='utf-8')
    shape = make_shape()
    AnnotationSaver.save((shape,), DummyAdapter, file_path, json_data=None, backup=True)
    # Оригинал должен остаться
    assert file_path.exists()
    # Должен появиться backup
    backups = list(tmp_path.glob("backup_me_backup_*.json"))
    assert backups, "No backup file created"


def test_adapter_without_shapes_to_json_raises(tmp_path):
    file_path = tmp_path / "err.json"
    file_path.write_text('{}', encoding='utf-8')
    class BadAdapter:
        pass
    shape = make_shape()
    with pytest.raises(NotImplementedError):
        AnnotationSaver.save((shape,), BadAdapter, file_path, json_data=None)


def test_write_json_to_file(tmp_path):
    file_path = tmp_path / "write.json"
    data = {"a": 123}
    AnnotationSaver._write_json_to_file(data, file_path)
    assert json.loads(file_path.read_text(encoding='utf-8')) == {"a": 123}


def test_make_backup_creates_copy(tmp_path):
    file_path = tmp_path / "myfile.json"
    file_path.write_text('{"a":1}', encoding='utf-8')
    AnnotationSaver._make_backup(file_path)
    backups = list(tmp_path.glob("myfile_backup_*.json"))
    assert backups, "Backup not found"
    assert backups[0].read_text(encoding='utf-8') == '{"a":1}'


def test_make_backup_does_nothing_if_not_exists(tmp_path):
    file_path = tmp_path / "notexist.json"
    # Не должно бросить ошибку
    AnnotationSaver._make_backup(file_path)
    # Не должно появиться файлов
    assert not list(tmp_path.glob("notexist_backup_*.json"))
