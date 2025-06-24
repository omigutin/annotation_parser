import json
import shutil
import tempfile
from pathlib import Path

import pytest

from annotation_parser.adapters.labelme_adapter import LabelMeAdapter
from annotation_parser.core.annotation_saver import AnnotationSaver
from annotation_parser.shape import Shape
from annotation_parser.public_enums import ShapeType


@pytest.fixture
def tmp_file_path(tmp_path):
    # Temporary file for save/load tests
    file = tmp_path / "test_labelme_save.json"
    return file


@pytest.fixture
def minimal_labelme_json():
    # Минимальный валидный JSON LabelMe для сохранения
    return {
        "shapes": [{
            "label": "cat",
            "points": [[1, 2], [3, 4]],
            "shape_type": "rectangle"
        }],
        "imagePath": "img.png",
        "imageHeight": 100,
        "imageWidth": 200
    }


@pytest.fixture
def minimal_shape():
    return Shape(
        label="cat",
        coords=[[1, 2], [3, 4]],
        type=ShapeType.RECTANGLE
    )


def test_save_and_reload_labelme(tmp_file_path, minimal_labelme_json, minimal_shape):
    # Save shape → reload → check shape equality
    shapes = (minimal_shape,)
    # Save to file
    AnnotationSaver.save(
        shapes=shapes,
        adapter=LabelMeAdapter,
        file_path=tmp_file_path,
        json_data=minimal_labelme_json,
        backup=False
    )
    # Read file
    with open(tmp_file_path, "r", encoding="utf-8") as f:
        result = json.load(f)
    assert "shapes" in result
    assert result["shapes"][0]["label"] == "cat"
    assert result["shapes"][0]["points"] == [[1.0, 2.0], [3.0, 2.0], [3.0, 4.0], [1.0, 4.0]]


def test_save_creates_backup(tmp_file_path, minimal_labelme_json, minimal_shape):
    # Create file first
    shapes = (minimal_shape,)
    tmp_file_path.write_text(json.dumps(minimal_labelme_json), encoding="utf-8")
    # Save again with backup
    AnnotationSaver.save(
        shapes=shapes,
        adapter=LabelMeAdapter,
        file_path=tmp_file_path,
        json_data=minimal_labelme_json,
        backup=True
    )
    # Backup file should exist
    parent = tmp_file_path.parent
    backups = list(parent.glob(f"{tmp_file_path.stem}_backup_*{tmp_file_path.suffix}"))
    assert backups, "Backup file not found"


def test_save_invalid_adapter(tmp_file_path, minimal_labelme_json, minimal_shape):
    # Адаптер без shapes_to_json
    class BadAdapter:
        pass

    with pytest.raises(NotImplementedError):
        AnnotationSaver.save(
            shapes=(minimal_shape,),
            adapter=BadAdapter,
            file_path=tmp_file_path,
            json_data=minimal_labelme_json,
            backup=False
        )


def test_save_invalid_file_path(tmp_path, minimal_labelme_json, minimal_shape):
    # Попытка сохранить в несуществующую директорию
    bad_path = tmp_path / "nonexistent_dir" / "file.json"
    with pytest.raises(FileNotFoundError):
        AnnotationSaver.save(
            shapes=(minimal_shape,),
            adapter=LabelMeAdapter,
            file_path=bad_path,
            json_data=minimal_labelme_json,
            backup=False
        )
