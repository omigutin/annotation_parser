"""
    run.py — универсальный демо-скрипт для локального тестирования парсера AnnotationParser.
    Запускается из корня проекта. Требует наличие tests/labelme/labelme_test.json.
"""

from pathlib import Path

from src.annotation_parser.api.shapes_api import (
    get_shapes_by_label,
    filter_shapes,
)
from src.annotation_parser import Shape, create, parse_labelme, save_labelme
from src.annotation_parser.public_enums import ShapeType


def divider(title: str = ""):
    print(f"\n{'=' * 10} {title} {'=' * 10}" if title else "\n" + "=" * 30)


def main():
    labelme_demo()
    shapes_api_demo()


def labelme_demo():
    print("=== DEMO: AnnotationParser (LabelMe only) ===")
    file = Path(__file__).parent / "tests/labelme/labelme_test.json"
    out_path = file.parent / "labelme_test_out.json"

    # Тест 1: ООП стиль
    divider("ООП стиль (AnnotationFile)")
    try:
        parser = create(file, 'labelme')
        shapes = parser.parse()
        print(f"Parsed {len(shapes)} shapes:")
        for shape in shapes:
            print(" —", shape)
        parser.save(shapes, backup=True)
        print(f"Shapes saved to '{file}'.")
    except Exception as e:
        print(f"Ошибка парсинга через AnnotationFile: {e}")
        shapes = ()

    # Тест 2: Функциональный стиль
    divider("Функциональный стиль")
    try:
        shapes2 = parse_labelme(file)
        print(f"Parsed {len(shapes2)} shapes:")
        for shape in shapes2:
            print(" —", shape)
    except Exception as e:
        print(f"Ошибка парсинга через parse_labelme: {e}")

    # Тест 3: Сохранение
    divider("Сохранение")
    try:
        save_labelme(shapes, out_path, backup=True)
        print(f"Saved shapes to {out_path} (backup enabled).")
    except Exception as e:
        print(f"Ошибка при сохранении: {e}")

    # Тест 4: Фильтрация по несуществующему лейблу (через функцию)
    divider("Фильтрация: несуществующий лейбл")
    try:
        shapes_dog = get_shapes_by_label(shapes, "dog")
        print(f"Shapes with label 'dog': {len(shapes_dog)} (ожидается 0)")
    except Exception as e:
        print(f"Ошибка фильтрации: {e}")

    # Тест 5: Фильтрация по существующему лейблу (через функцию)
    divider("Фильтрация: существующий лейбл")
    try:
        shapes_crop = get_shapes_by_label(shapes, "crop")
        print(f"Shapes with label 'crop': {len(shapes_crop)}")
        if shapes_crop:
            print("Пример:", shapes_crop[0])
    except Exception as e:
        print(f"Ошибка фильтрации: {e}")

    # Тест 6: Ошибка — неверный путь
    divider("[ERROR] неверный путь")
    try:
        parser_bad = create(file.parent / "not_exists.json", 'labelme')
        parser_bad.parse()
    except Exception as e:
        print(f"[ERROR] {e}")

    # Тест 7: Ошибка — некорректный JSON
    divider("[ERROR] некорректный JSON")
    bad_json_path = file.parent / "bad.json"
    try:
        with open(bad_json_path, "w", encoding="utf-8") as f:
            f.write("{not valid json]")  # Явно битый json
        try:
            parser_bad_json = create(bad_json_path, 'labelme')
            parser_bad_json.parse()
        except Exception as e2:
            print(f"[ERROR] {e2}")
    finally:
        if bad_json_path.exists():
            bad_json_path.unlink()

    # Тест 8: Фильтрация по предикату (shape.coords длинее 3)
    divider("Фильтрация: по произвольному предикату")
    try:
        shapes_large = filter_shapes(shapes, lambda shape: hasattr(shape, "coords") and len(shape.coords) > 3)
        print(f"Shapes with >3 coords: {len(shapes_large)}")
        if shapes_large:
            print("Пример:", shapes_large[0])
    except Exception as e:
        print(f"Ошибка при фильтрации: {e}")

    divider("THE END")


def shapes_api_demo():
    divider("shapes_api: демо-фильтрация")
    shapes = (
        Shape(label="person", coords=[[1, 2], [3, 4]], type=ShapeType.RECTANGLE, number=1, wz_number=2),
        Shape(label="car", coords=[[5, 6], [7, 8]], type=ShapeType.RECTANGLE, number=None, wz_number=2),
        Shape(label="person", coords=[[2, 2], [4, 4]], type=ShapeType.RECTANGLE, number=2, wz_number=3),
    )

    divider("Фильтрация по label == 'person'")
    persons = filter_shapes(shapes, lambda s: s.label == "person")
    print(persons)

    divider("Фильтрация по wz_number == 2")
    zone2 = filter_shapes(shapes, lambda s: s.wz_number == 2)
    print(zone2)

    divider("Только индивидуальные 'person'")
    persons_indiv = filter_shapes(shapes, lambda s: s.label == "person", individual=True, common=False)
    print(persons_indiv)

    divider("Только общие фигуры (без number)")
    common_shapes = filter_shapes(shapes, lambda s: True, individual=False, common=True)
    print(common_shapes)

    divider("Сложный предикат (person & wz_number==2, только общие)")
    complex_case = filter_shapes(
        shapes,
        lambda s: s.label == "person" and s.wz_number == 2,
        individual=False,
        common=True,
    )
    print(complex_case)


if __name__ == "__main__":
    main()
