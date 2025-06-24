import pytest
from pathlib import Path

from annotation_parser.core.annotation_file import AnnotationFile
from annotation_parser.public_enums import Adapters
from annotation_parser.shape import Shape

LABELME_JSON = Path(__file__).parent.parent / "labelme_test.json"


@pytest.fixture
def labelme_file():
    return LABELME_JSON


def test_parse_labelme_file(labelme_file):
    afile = AnnotationFile(labelme_file, Adapters.labelme, keep_json=True)
    shapes = afile.parse()
    assert isinstance(shapes, tuple)
    assert all(isinstance(s, Shape) for s in shapes)
    assert len(shapes) > 0
    # Основная sanity-проверка
    labels = {s.label for s in shapes}
    assert labels


def test_save_and_reload(tmp_path, labelme_file):
    afile = AnnotationFile(labelme_file, Adapters.labelme, keep_json=True)
    shapes = afile.parse()
    save_path = tmp_path / "out_labelme.json"
    # Сначала только для сохранения (без чтения несуществующего файла)
    afile2 = AnnotationFile(save_path, Adapters.labelme, keep_json=False, validate_file=False)
    afile2.save(shapes, backup=False)
    # Потом — открываем для чтения, когда файл уже есть
    afile3 = AnnotationFile(save_path, Adapters.labelme, keep_json=True)
    shapes2 = afile3.parse()
    assert len(shapes2) == len(shapes)
    labels1 = [s.label for s in shapes]
    labels2 = [s.label for s in shapes2]
    assert labels1 == labels2
