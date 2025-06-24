import pytest


def check_adapter_load_and_save(adapter_cls, minimal_json, minimal_shape):
    """Универсальный контракт для адаптеров — load и shapes_to_json должны быть реализованы и согласованы."""
    # Проверка наличия методов
    assert hasattr(adapter_cls, "load")
    assert hasattr(adapter_cls, "shapes_to_json")

    # Загружаем Shape из минимального валидного json
    shapes = adapter_cls.load(minimal_json)
    assert isinstance(shapes, tuple)
    assert all(isinstance(s, type(minimal_shape)) for s in shapes)

    # Сохраняем обратно в json
    result_json = adapter_cls.shapes_to_json(minimal_json, shapes)
    assert isinstance(result_json, dict)

    # Проверка round-trip: загруженный shape → json → shape, структура не теряется (по ключевым полям)
    shapes2 = adapter_cls.load(result_json)
    # Проверим хотя бы количество фигур и основные поля
    assert len(shapes) == len(shapes2)
    assert shapes2[0].label == shapes[0].label


def check_adapter_invalid_json(adapter_cls):
    """adapter.load должен кидать ValueError на некорректный json"""
    with pytest.raises(ValueError):
        adapter_cls.load({"not_shapes": []})
