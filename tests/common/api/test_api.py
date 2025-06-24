import pytest
import sys

from annotation_parser.api.api import available_adapters, create


# Подгружаем модуль через sys.modules для monkeypatch
api_mod = sys.modules['annotation_parser.api.api']


class DummyAnnotationFile:
    def parse(self):
        return ("shape1",)


def test_available_adapters_returns_list(monkeypatch):
    monkeypatch.setattr(api_mod.AdapterFactory, "list_adapters", lambda: ["labelme", "coco"])
    adapters = available_adapters()
    assert isinstance(adapters, list)
    assert "labelme" in adapters


def test_create_returns_parser_with_parse(monkeypatch):
    monkeypatch.setattr(api_mod, "AnnotationFile", lambda *a, **kw: DummyAnnotationFile())
    parser = create("dummy_path.json", "labelme")
    assert hasattr(parser, "parse")
    assert isinstance(parser.parse(), tuple)


def test_create_invalid_path_raises(monkeypatch):
    def raise_file_not_found(*a, **kw): raise FileNotFoundError
    monkeypatch.setattr(api_mod, "AnnotationFile", raise_file_not_found)
    with pytest.raises(FileNotFoundError):
        create("not_exists.json", "labelme")
