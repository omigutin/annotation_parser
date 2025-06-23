import pytest
from unittest.mock import patch, MagicMock

import your_module.annotation_parser as ap


@pytest.fixture
def dummy_shapes():
    # Просто мок-объекты Shape
    class DummyShape:
        pass
    return (DummyShape(), DummyShape())


@pytest.fixture
def dummy_path(tmp_path):
    # Временный путь для файлов
    return tmp_path / "dummy.json"


def test_available_adapters_delegates_to_factory():
    with patch.object(ap.AdapterFactory, "list_adapters", return_value=["labelme", "coco"]):
        adapters = ap.available_adapters()
        assert adapters == ["labelme", "coco"]


def test_create_returns_annotationfile_instance():
    with patch.object(ap, "AnnotationFile") as mock_file:
        instance = MagicMock()
        mock_file.return_value = instance
        result = ap.create("file.json", "labelme")
        mock_file.assert_called_once_with("file.json", "labelme", keep_json=True, shift_point=None)
        assert result is instance


def test_parse_calls_annotationfile_parse():
    mock_instance = MagicMock()
    with patch.object(ap, "AnnotationFile") as mock_file:
        mock_file.return_value = mock_instance
        mock_instance.parse.return_value = ("a", "b")
        result = ap.parse("file.json", "labelme")
        assert result == ("a", "b")
        mock_instance.parse.assert_called_once()


@pytest.mark.parametrize("func,adapter", [
    (ap.parse_labelme, ap.Adapters.labelme),
    (ap.parse_coco, ap.Adapters.coco),
    (ap.parse_voc, ap.Adapters.voc),
])
def test_parse_shortcuts_delegate_correctly(func, adapter):
    with patch.object(ap, "parse") as mock_parse:
        mock_parse.return_value = ("s",)
        result = func("f.json")
        mock_parse.assert_called_once_with("f.json", adapter, shift_point=None)
        assert result == ("s",)


def test_save_raises_on_missing_file_path(dummy_shapes):
    with pytest.raises(ValueError):
        ap.save(dummy_shapes, None, "labelme")


def test_save_raises_on_missing_markup_type(dummy_shapes, dummy_path):
    with pytest.raises(ValueError):
        ap.save(dummy_shapes, dummy_path, None)


def test_save_calls_annotationfile_save(dummy_shapes, dummy_path):
    mock_instance = MagicMock()
    with patch.object(ap, "AnnotationFile") as mock_file:
        mock_file.return_value = mock_instance
        ap.save(dummy_shapes, dummy_path, "labelme", backup=True)
        mock_file.assert_called_once_with(dummy_path, "labelme", keep_json=True, validate_file=False)
        mock_instance.save.assert_called_once_with(dummy_shapes, backup=True)


@pytest.mark.parametrize("func,adapter", [
    (ap.save_labelme, ap.Adapters.labelme),
    (ap.save_coco, ap.Adapters.coco),
    (ap.save_voc, ap.Adapters.voc),
])
def test_save_shortcuts_delegate_correctly(func, adapter, dummy_shapes, dummy_path):
    with patch.object(ap, "save") as mock_save:
        func(dummy_shapes, dummy_path, backup=False)
        mock_save.assert_called_once_with(dummy_shapes, dummy_path, adapter, False)


def test_create_with_shift_point():
    with patch.object(ap, "AnnotationFile") as mock_file:
        instance = MagicMock()
        mock_file.return_value = instance
        result = ap.create("f.json", "coco", shift_point=(1, 2))
        mock_file.assert_called_once_with("f.json", "coco", keep_json=True, shift_point=(1, 2))
        assert result is instance
