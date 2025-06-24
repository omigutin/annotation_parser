import pytest
import sys
from annotation_parser.api.saver_api import save

# Получаем модуль saver_api для monkeypatch (работает даже при from .api import *)
saver_api_mod = sys.modules['annotation_parser.api.saver_api']


class DummyShape:
    pass

def test_save_calls_annotationfile(monkeypatch, tmp_path):
    called = {}

    def DummyAF(*a, **kw):
        def save_method(*args, **kwargs):
            called["ok"] = True
        return type("AF", (), {"save": save_method})()
    # Важно: monkeypatch через объект модуля!
    monkeypatch.setattr(saver_api_mod, "AnnotationFile", DummyAF)
    save((DummyShape(),), tmp_path / "file.json", "labelme")
    assert "ok" in called


def test_save_invalid_path_raises(monkeypatch):
    def DummyAF(*a, **kw):
        raise FileNotFoundError
    monkeypatch.setattr(saver_api_mod, "AnnotationFile", DummyAF)
    with pytest.raises(FileNotFoundError):
        save((DummyShape(),), "not_exists/file.json", "labelme")
