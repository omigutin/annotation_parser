# How To Use Annotation Parser

## Parsing Annotation Data

**1. Initialize the parser and parse shapes explicitly:**

```python
parser = create('path/to/annotations.json', 'labelme')
shapes = parser.parse()
```

**2. Initialize and parse shapes in a single line:**

```python
shapes = create('path/to/annotations.json', 'labelme').parse()
```

**3. Parse directly with a universal function:**

```python
shapes = parse('path/to/annotations.json', 'labelme')
```

**4. Parse with a specialized function for a specific format:**

```python
shapes = parse_labelme('annotations.json')
shapes = parse_coco('annotations.json')
shapes = parse_voc('annotations.json')
```

---

## Saving Annotation Data

### Via AnnotationFile object (stateful mode)

**A. Save into the original file (with backup):**

```python
parser = create('annotations.json', 'labelme', keep_json=True)
shapes = parser.parse()
# ...modify shapes...
parser.save(shapes)  # Saves to 'annotations.json', creates a backup if file exists.
```

**B. Save into a new file:**

```python
parser.save(shapes, new_path='new_annotations.json')
# 'annotations.json' remains unchanged, new file written.
```

### Via universal API function (stateless mode)

**A. Save shapes into any file (with backup if file exists):**

```python
save(shapes, 'output.json', 'labelme')
save(shapes, 'output.json', Adapters.labelme)
```

### Via format-specific API function

**A. Save as LabelMe/COCO/VOC (with backup if file exists):**

```python
save_labelme(shapes, 'labelme.json')
save_coco(shapes, 'coco.json')
save_voc(shapes, 'voc.json')
```

---

## File Overwrite and Backup

* **If the target file exists**, it is automatically backed up with a timestamp before overwriting.
* Backups are stored in the same directory as the original file, with the pattern:
  `<filename>_backup_<YYYYMMDD_HHMMSS>.json`

---

## Available Adapters

* Call `available_adapters()` to get the list of currently registered formats.
* Use the `Adapters` enum for strict type checking and autocompletion in your code.

---

## Additional Notes

* All parsing and saving functions support `shift_point` for geometric transformation if needed.
* You can always work in both “stateful” (object-oriented) and “stateless” (functional) style, whichever is more convenient for your task.
* Backups ensure data safety and auditability, even if you overwrite the same file many times.

---
