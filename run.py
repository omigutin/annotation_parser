# run.py — ручной запуск и примеры AnnotationParser

from pathlib import Path

from src.annotation_parser import create, parse_labelme, save_labelme, parse


def main():
    print("=== DEMO: AnnotationParser ===")

    # Демонстрация: чтение и вывод фигур из LabelMe файла
    file = Path(__file__).resolve().parent / "tests/labelme/labelme_test.json"

    # ООП-стиль: через объект AnnotationFile
    parser = create(file, 'labelme')
    shapes = parser.parse()
    print(f"Parsed {len(shapes)} shapes via OOP-style (AnnotationFile):")
    for shape in shapes:
        print(" —", shape)

    # Функциональный стиль: напрямую одной строкой
    shapes2 = parse_labelme(file)
    print(f"\nParsed {len(shapes2)} shapes via functional style:")
    for shape in shapes2:
        print(" —", shape)

    # Демонстрация сохранения (в отдельный файл, с backup)
    out_path = file.parent / "labelme_test_out.json"
    save_labelme(shapes, out_path, backup=True)
    print(f"\nSaved shapes to {out_path} with backup enabled.")

    # Можно добавить мини-тест фильтрации по лейблу:
    shapes_cats = parser.get_shapes_by_label("cat")
    print(f"\nFound {len(shapes_cats)} shapes with label 'cat'")


if __name__ == "__main__":
    main()
