# run.py — универсальный демо-скрипт для локального тестирования парсера AnnotationParser

from pathlib import Path

from src.annotation_parser.api import filter_shapes
from src.annotation_parser import Shape
from src.annotation_parser import create, parse_labelme, save_labelme


def divider(title: str = ""):
    print(f"\n{'=' * 10} {title} {'=' * 10}" if title else "\n" + "=" * 30)


def main():
    labelme()
    shapes_api()


def labelme():
    print("=== DEMO: AnnotationParser (LabelMe only) ===")
    file = Path(__file__).resolve().parent / "tests/labelme/labelme_test.json"
    out_path = file.parent / "labelme_test_out.json"

    # Тест 1: Корректная работа — ООП стиль
    divider("ООП стиль (AnnotationFile)")
    try:
        parser = create(file, 'labelme')
        shapes = parser.parse()
        print(f"Parsed {len(shapes)} shapes:")
        for shape in shapes:
            print(" —", shape)
        shapes = parser.se()
        print(f"Parsed {len(shapes)} shapes:")
        for shape in shapes:
            print(" —", shape)
        parser.save(shapes, backup=True)
        print(f"Shapes saved to '{file}'.")
    except Exception as e:
        print(f"Ошибка парсинга через AnnotationFile: {e}")

    # Тест 2: Функциональный стиль
    divider("Функциональный стиль")
    try:
        shapes2 = parse_labelme(file)
        print(f"Parsed {len(shapes2)} shapes:")
        for shape in shapes2:
            print(" —", shape)
    except Exception as e:
        print(f"Ошибка парсинга через parse_labelme: {e}")

    # Тест 3: Сохранение с backup
    divider("Сохранение")
    try:
        save_labelme(shapes, out_path, backup=True)
        print(f"Saved shapes to {out_path} (backup enabled).")
    except Exception as e:
        print(f"Ошибка при сохранении: {e}")

    # Тест 4: Фильтрация по несуществующему лейблу
    divider("Фильтрация: несуществующий лейбл")
    shapes_dog = parser.get_shapes_by_label("dog")
    print(f"Shapes with label 'dog': {len(shapes_dog)} (ожидается 0)")

    # Тест 5: Фильтрация по существующему лейблу
    divider("Фильтрация: существующий лейбл")
    shapes_cat = parser.get_shapes_by_label("crop")
    print(f"Shapes with label 'crop': {len(shapes_cat)}")
    if shapes_cat:
        print("Пример:", shapes_cat[0])

    # Тест 6: Ошибка — неверный путь
    divider("[ERROR] неверный путь")
    try:
        parser_bad = create(file.parent / "not_exists.json", 'labelme')
        parser_bad.parse()
    except Exception as e:
        print(f"[ERROR] {e}")

    # Тест 7: Ошибка — некорректный JSON
    divider("[ERROR] некорректный JSON")
    try:
        # создадим временный файл с некорректным JSON
        bad_json_path = file.parent / "bad.json"
        with open(bad_json_path, "w", encoding="utf-8") as f:
            f.write("{not valid json]")
        try:
            parser_bad_json = create(bad_json_path, 'labelme')
            parser_bad_json.parse()
        except Exception as e2:
            print(f"[ERROR] {e2}")
        finally:
            bad_json_path.unlink()
    except Exception as e:
        print(f"Ошибка при тесте с некорректным JSON: {e}")

    # Тест 8: Фильтрация по предикату
    divider("Фильтрация: по произвольному предикату")
    shapes_large = parser.filter_shapes(lambda shape: hasattr(shape, "coords") and len(shape.coords) > 3)
    print(f"Shapes with >3 coords: {len(shapes_large)}")
    if shapes_large:
        print("Пример:", shapes_large[0])

    divider("THE END")


def shapes_api():
    # Допустим, у нас есть кортеж фигур
    shapes = (
        Shape(label="person", coords=[[1, 2], [3, 4]], type=None, number=1, wz_number=2),
        Shape(label="car", coords=[[5, 6], [7, 8]], type=None, number=None, wz_number=2),
        Shape(label="person", coords=[[2, 2], [4, 4]], type=None, number=2, wz_number=3),
    )

    # 1. Найти все фигуры с label == "person"
    persons = filter_shapes(shapes, lambda s: s.label == "person")
    print(persons)
    # → tuple из двух Shape с label 'person'

    # 2. Найти все фигуры, относящиеся к рабочей зоне 2
    zone2 = filter_shapes(shapes, lambda s: s.wz_number == 2)
    print(zone2)
    # → две фигуры: "person" и "car" (wz_number=2)

    # 3. Найти все индивидуальные фигуры с label "person"
    persons_indiv = filter_shapes(
        shapes,
        lambda s: s.label == "person",
        individual=True,
        common=False,
    )
    print(persons_indiv)
    # → только индивидуальные "person" (т.е. те, у кого .number не None)

    # 4. Найти только общие фигуры (без number), с любым label
    common_shapes = filter_shapes(
        shapes,
        lambda s: True,
        individual=False,
        common=True,
    )
    print(common_shapes)
    # → фигуры, у которых .number is None

    # 5. Сложные фильтры: например, все "person" в рабочей зоне 2, только общие
    complex = filter_shapes(
        shapes,
        lambda s: s.label == "person" and s.wz_number == 2,
        individual=False,
        common=True,
    )
    print(complex)


if __name__ == "__main__":
    main()
