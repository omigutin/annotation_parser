# ![Python](https://img.icons8.com/color/32/python.png) AnnotationParser

> 🇷🇺   [Read in Russian](README.ru.md)

AnnotationParser is a universal Python library that parses annotation files from various formats (LabelMe, COCO, VOC, etc.) and converts them into a single, unified `Shape` type.
This approach allows you to read, filter, and save shapes using the same interface, regardless of the original annotation format.

> **Note:**
> Currently only the **LabelMe** format is fully implemented and tested.
> Other formats are planned for future releases (see [Limitations & Roadmap](#limitations--roadmap)).

---

## Table of Contents

* [Features](#features)
* [Usage Examples](#usage-examples)
* [Command-Line Interface (CLI)](#command-line-interface-cli-experimental)
* [Supported Formats](#supported-formats)
* [Limitations & Roadmap](#limitations--roadmap)
* [Contributing](#contributing)
* [Development & Testing](#development--testing)
* [FAQ / Common Issues](#faq--common-issues)
* [Author](#author)
* [License](#license)

---

## Features

* Unified API for reading, saving, and filtering shapes in annotation files
* Converts any supported format into a universal `Shape` type for downstream processing
* Extensible adapter system for multiple formats (LabelMe, COCO, VOC, ...)
* Functional and OOP usage styles
* High-level filtering and transformation functions for shape objects
* Clean, type-safe, and well-documented codebase

---

## Usage Examples

### Installation

> **Python 3.10+ required**

Install with pip (recommended for most users):

```bash
pip install annotation-parser
```

Or, if you have the source code locally:

```bash
pip install -e .
```

### Parse and Filter (LabelMe)

```python
from annotation_parser import create, get_shapes_by_label

file = "tests/labelme/labelme_test.json"
parser = create(file, "labelme")
shapes = parser.parse()  # tuple of Shape

# Get all shapes with label "person"
persons = get_shapes_by_label(shapes, "person")
print(persons)
```

### Save Annotations

```python
from annotation_parser import save_labelme

save_labelme(shapes, "result.json", backup=True)
```

### Filter by Working Zone, Group Number, Custom Predicate

```python
from annotation_parser import get_shapes_by_wz_number, get_shapes_by_number, filter_shapes

# Filter by working zone (wz_number)
zone2 = get_shapes_by_wz_number(shapes, wz_number=2)

# Filter by instance/group number
group_1 = get_shapes_by_number(shapes, number=1)

# Filter with any condition (lambda)
big_shapes = filter_shapes(shapes, lambda s: hasattr(s, "coords") and len(s.coords) > 3)
```

### OOP Style (Advanced)

```python
from annotation_parser import create

parser = create("tests/labelme/labelme_test.json", "labelme")
shapes = parser.parse()
# You can call parser.save(), parser.parse(), parser.filter_shapes() if needed
```

### Functional Style (shortcut)

```python
from annotation_parser import parse_labelme

shapes = parse_labelme("tests/labelme/labelme_test.json")
```

---

## Command-Line Interface (CLI) \[experimental]

> **Experimental!** Not fully tested.
> See [cli.py](src/annotation_parser/cli.py) for current options.

```bash
python cli.py parse --file tests/labelme/labelme_test.json --adapter labelme
python cli.py save --file tests/labelme/labelme_test.json --adapter labelme --out result.json --backup
python cli.py filter --file tests/labelme/labelme_test.json --adapter labelme --label crop
```

---

## Supported Formats

| Format      | Status           |
| ----------- | ---------------- |
| **LabelMe** | ✅ Supported      |
| COCO        | 🕑 Planned       |
| Pascal VOC  | 🕑 Planned       |
| YOLO        | 🕑 Planned       |
| ...         | (Suggest yours!) |

> 💡 **Want to see your annotation format supported?**
> Open an [issue or PR](https://github.com/omigutin/annotation_parser/issues) — or help me implement a new adapter!
> Any contribution or feedback on new formats is very welcome.

---

## Limitations & Roadmap

* **LabelMe** format is currently the only one fully implemented and tested.
* Adapters for other formats (COCO, Pascal VOC, YOLO, etc.) are planned, not yet implemented.
* Standard logging (with configurable log levels and error handling) will be added in future releases.
* The command-line interface (`cli.py`) is experimental and not fully tested; improvements needed.

---

## Contributing

* PRs, bug reports, and suggestions are welcome!
* For new formats, contribute an adapter in `src/annotation_parser/adapters/`
* All code should be type-checked (`mypy`), formatted (`black`), and covered by tests (`pytest`).

---

## Development & Testing

* Install dev dependencies:

  ```bash
  poetry install --with dev
  ```
* Run tests:

  ```bash
  pytest
  ```

---

## FAQ / Common Issues

**Q: Why do only LabelMe files work?**
A: Only the LabelMe adapter is currently implemented. COCO/VOC support is planned.

**Q: CLI throws errors or doesn't work as expected?**
A: `cli.py` is not fully tested. Check [Limitations & Roadmap](#limitations--roadmap) and use the Python API for production.

---

## Author

[![Telegram](https://img.shields.io/badge/-Telegram-26A5E4?style=flat\&logo=telegram\&logoColor=white)](https://t.me/omigutin)
[![GitHub](https://img.shields.io/badge/-GitHub-181717?style=flat\&logo=github\&logoColor=white)](https://github.com/omigutin)

**Project:** [github.com/omigutin/annotation\_parser](https://github.com/omigutin/annotation_parser)
**Project Tracker:** [annotation\_parser Project Board](https://github.com/users/omigutin/projects/2)
Contact: [migutin83@yandex.ru](mailto:migutin83@yandex.ru)

---

## License

MIT License.
See [LICENSE](LICENSE) for details.
