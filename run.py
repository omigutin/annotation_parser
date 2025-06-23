# run.py — универсальный демо-скрипт для локального тестирования парсера AnnotationParser

from pathlib import Path

from src.annotation_parser import create, parse_labelme, save_labelme


def divider(title: str = ""):
    print(f"\n{'=' * 10} {title} {'=' * 10}" if title else "\n" + "=" * 30)


def main():
    labelme()


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
    divider("Ошибка: неверный путь")
    try:
        parser_bad = create(file.parent / "not_exists.json", 'labelme')
        parser_bad.parse()
    except Exception as e:
        print(f"Ожидаемая ошибка: {e}")

    # Тест 7: Ошибка — некорректный JSON
    divider("Ошибка: некорректный JSON")
    try:
        # создадим временный файл с некорректным JSON
        bad_json_path = file.parent / "bad.json"
        with open(bad_json_path, "w", encoding="utf-8") as f:
            f.write("{not valid json]")
        try:
            parser_bad_json = create(bad_json_path, 'labelme')
            parser_bad_json.parse()
        except Exception as e2:
            print(f"Ожидаемая ошибка: {e2}")
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


if __name__ == "__main__":
    main()
