import pytest


def check_adapter_methods(adapter_cls):
    """Контракт: у адаптера должны быть реализованы обязательные методы."""
    assert hasattr(adapter_cls, "load"), "Adapter must have staticmethod `load`"
    assert hasattr(adapter_cls, "shapes_to_json"), "Adapter must have staticmethod `shapes_to_json`"


def check_adapter_load_type(adapter_cls, minimal_json, shape_type):
    """load должен возвращать кортеж нужных Shape-объектов"""
    shapes = adapter_cls.load(minimal_json)
    assert isinstance(shapes, tuple), f"Adapter.load should return tuple, got {type(shapes)}"
    assert all(isinstance(s, shape_type) for s in shapes)


def check_adapter_round_trip(adapter_cls, minimal_json, shape_type):
    """Проверяет, что shape → json → shape не теряет данные по ключевым полям"""
    shapes1 = adapter_cls.load(minimal_json)
    result_json = adapter_cls.shapes_to_json(minimal_json, shapes1)
    shapes2 = adapter_cls.load(result_json)
    assert len(shapes1) == len(shapes2)
    for a, b in zip(shapes1, shapes2):
        assert a.label == b.label
        assert a.type == b.type
        # Можно проверить coords с округлением
        assert all(abs(x1 - x2) < 1e-5 and abs(y1 - y2) < 1e-5
                   for (x1, y1), (x2, y2) in zip(a.coords, b.coords))


def check_adapter_invalid_json(adapter_cls):
    with pytest.raises(ValueError):
        adapter_cls.load({"not_shapes": []})


def check_adapter_shift_point(adapter_cls, minimal_json, shape_type):
    """Проверяет смещение координат через shift_point (если поддерживается)"""
    shift = (100, 50)
    shapes = adapter_cls.load(minimal_json, shift_point=shift)
    # Просто проверяем, что coords сдвинуты, если shift_point используется
    # Предполагаем, что первая координата сместится на -shift
    if shapes:
        orig = minimal_json["shapes"][0]["points"][0]
        new = shapes[0].shifted_coords[0]
        assert abs(new[0] - (orig[0] - shift[0])) < 1e-5
        assert abs(new[1] - (orig[1] - shift[1])) < 1e-5
