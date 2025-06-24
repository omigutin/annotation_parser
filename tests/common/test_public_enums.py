import pytest


def check_enum_contract(enum_cls, expected_values: list):
    """Проверяет, что Enum содержит все ожидаемые значения и только их."""
    values = [e.value for e in enum_cls]
    # Все значения есть в enum
    for val in expected_values:
        assert val in values, f"Missing expected value {val} in {enum_cls.__name__}"
    # Нет лишних
    assert set(values) == set(expected_values), f"Unexpected values in {enum_cls.__name__}: {set(values) ^ set(expected_values)}"
    # Проверка уникальности
    assert len(set(values)) == len(values), f"Enum {enum_cls.__name__} has duplicate values"

# ————
# Пример использования для твоих enum-классов


from annotation_parser.public_enums import Adapters, ShapeType, ShapePosition


def test_adapters_enum():
    check_enum_contract(Adapters, ["labelme", "coco", "voc"])


def test_shape_type_enum():
    check_enum_contract(ShapeType, ["line", "point", "polygon", "rectangle"])


def test_shape_position_enum():
    check_enum_contract(ShapePosition, ["left", "right", "top", "bottom", "centre"])
