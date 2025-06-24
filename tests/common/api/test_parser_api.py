import pytest
import sys

from annotation_parser.api.parser_api import parse

parser_api_mod = sys.modules['annotation_parser.api.parser_api']


def test_parse_returns_tuple(monkeypatch):
    def dummy_parse(*a, **kw): return ("shape1", "shape2")
    # Патчим не строкой, а через модуль!
    monkeypatch.setattr(parser_api_mod, "AnnotationFile", lambda *a, **kw: type("Ann", (), {"parse": dummy_parse})())
    result = parse("dummy.json", "labelme")
    assert isinstance(result, tuple)
    assert len(result) == 2


def test_parse_invalid_path_raises(monkeypatch):
    def raise_file_not_found(*a, **kw): raise FileNotFoundError
    monkeypatch.setattr(parser_api_mod, "AnnotationFile", raise_file_not_found)
    with pytest.raises(FileNotFoundError):
        parse("not_exists.json", "labelme")
