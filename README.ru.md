# ![Python](https://img.icons8.com/color/32/python.png) AnnotationParser

> [Читать по-английски](README.md)

AnnotationParser — универсальная Python-библиотека для парсинга файлов разметки в различных форматах (LabelMe, COCO, VOC и др.) и преобразования их к единому универсальному типу `Shape`.
Такой подход позволяет читать, фильтровать и сохранять фигуры через единый интерфейс, вне зависимости от исходного формата аннотаций.

> **Внимание:**
> На данный момент полностью реализован и протестирован только формат **LabelMe**.
> Поддержка других форматов запланирована (см. [Ограничения и планы](#ограничения--планы)).

---

## Оглавление

* [Возможности](#возможности)
* [Примеры использования](#примеры-использования)
* [Командная строка (CLI)](#командная-строка-cli-экспериментально)
* [Поддерживаемые форматы](#поддерживаемые-форматы)
* [Ограничения и планы](#ограничения--планы)
* [Как помочь проекту](#как-помочь-проекту)
* [Разработка и тестирование](#разработка-и-тестирование)
* [FAQ и распространённые вопросы](#faq-и-распространённые-вопросы)
* [Автор](#автор)
* [Лицензия](#лицензия)

---

## Возможности

* Единый API для чтения, сохранения и фильтрации фигур из файлов разметки
* Приведение любого поддерживаемого формата к универсальному типу `Shape` для дальнейшей работы
* Расширяемая система адаптеров для разных форматов (LabelMe, COCO, VOC ...)
* Функциональный и ООП-стили работы
* Высокоуровневые функции фильтрации и преобразования фигур
* Чистый, типизированный и документированный код

---

## Примеры использования

### Установка

> **Требуется Python 3.10+**

Установить через pip (рекомендуется):

```bash
pip install annotation-parser
```

Или из локального исходника:

```bash
pip install -e .
```

### Парсинг и фильтрация (LabelMe)

```python
from annotation_parser import create, get_shapes_by_label

file = "tests/labelme/labelme_test.json"
parser = create(file, "labelme")
shapes = parser.parse()  # tuple of Shape

# Получить все фигуры с label "person"
persons = get_shapes_by_label(shapes, "person")
print(persons)
```

### Сохранение аннотаций

```python
from annotation_parser import save_labelme

save_labelme(shapes, "result.json", backup=True)
```

### Фильтрация по рабочей зоне, номеру группы, произвольному фильтру

```python
from annotation_parser import get_shapes_by_wz_number, get_shapes_by_number, filter_shapes

# По номеру рабочей зоны (wz_number)
zone2 = get_shapes_by_wz_number(shapes, wz_number=2)

# По номеру экземпляра/группы
group_1 = get_shapes_by_number(shapes, number=1)

# По произвольному предикату (lambda)
big_shapes = filter_shapes(shapes, lambda s: hasattr(s, "coords") and len(s.coords) > 3)
```

### ООП-стиль (продвинутый)

```python
from annotation_parser import create

parser = create("tests/labelme/labelme_test.json", "labelme")
shapes = parser.parse()
# Можно вызвать parser.save(), parser.parse(), parser.filter_shapes() и др.
```

### Функциональный стиль (шорткат)

```python
from annotation_parser import parse_labelme

shapes = parse_labelme("tests/labelme/labelme_test.json")
```

---

## Командная строка (CLI) \[экспериментально]

> **Экспериментально!** Не полностью протестировано.
> Актуальные параметры см. в [cli.py](src/annotation_parser/cli.py).

```bash
python cli.py parse --file tests/labelme/labelme_test.json --adapter labelme
python cli.py save --file tests/labelme/labelme_test.json --adapter labelme --out result.json --backup
python cli.py filter --file tests/labelme/labelme_test.json --adapter labelme --label crop
```

---

## Поддерживаемые форматы

| Формат      | Статус              |
| ----------- | ------------------- |
| **LabelMe** | ✅ Поддерживается    |
| COCO        | 🕑 В планах         |
| Pascal VOC  | 🕑 В планах         |
| YOLO        | 🕑 В планах         |
| ...         | (Пишите пожелания!) |

> 💡 **Хотите видеть поддержку вашего формата?**
> Открывайте issue или PR: [omigutin/annotation\_parser/issues](https://github.com/omigutin/annotation_parser/issues)
> Приветствуются любые предложения и помощь с адаптерами!

---

## Ограничения & Планы

* Полноценно реализован и протестирован только формат **LabelMe**
* Адаптеры для COCO, Pascal VOC, YOLO и других — пока не реализованы
* В будущем будет добавлен стандартный logging с уровнями и обработкой ошибок
* CLI (`cli.py`) — экспериментальный, требует тестирования и доработки

---

## Как помочь проекту

* Любые PR, баг-репорты и предложения приветствуются!
* Все доработки, новые функции и исправления отправляются через Pull Request в ветку develop.
* Ветка main используется только для стабильных релизов.
* Для новых форматов добавляйте адаптеры в src/annotation_parser/adapters/.
* Перед мержем любые изменения проходят код-ревью.
* Весь код должен быть типизирован (mypy), отформатирован (black) и покрыт тестами (pytest).
* Создавайте Issue или предлагайте новый адаптер, даже если не готовы реализовать его сами.
* Хотите стать контрибьютором?
    Делайте форк, заводите ветку от develop, отправляйте Pull Request или пишите напрямую (см. контакты).
    Любая помощь и идеи по новым форматам приветствуются!

---

## Разработка и тестирование

* Установка зависимостей для разработки:

  ```bash
  poetry install --with dev
  ```
* Запуск тестов:

  ```bash
  pytest
  ```

---

## FAQ и распространённые вопросы

**Q: Почему работают только файлы LabelMe?**
A: Реализован только адаптер для LabelMe. Поддержка COCO/VOC запланирована.

**Q: CLI вызывает ошибки или не работает как надо?**
A: `cli.py` не полностью протестирован. См. [Ограничения и планы](#ограничения--планы) и используйте Python API для продакшена.

---

## Автор

[![Telegram](https://img.shields.io/badge/-Telegram-26A5E4?style=flat\&logo=telegram\&logoColor=white)](https://t.me/omigutin)
[![GitHub](https://img.shields.io/badge/-GitHub-181717?style=flat\&logo=github\&logoColor=white)](https://github.com/omigutin)

**Проект:** [github.com/omigutin/annotation\_parser](https://github.com/omigutin/annotation_parser)
**Трекер:** [annotation\_parser Project Board](https://github.com/users/omigutin/projects/2)
Контакт: [migutin83@yandex.ru](mailto:migutin83@yandex.ru)

---

## Лицензия

MIT License.
См. [LICENSE](LICENSE) для подробностей.
