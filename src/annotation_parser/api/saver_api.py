"""
    High-Level Annotation Saving API
    ===============================================

    This module provides top-level functions to save tuples of Shape objects
    to annotation files in supported formats (LabelMe, COCO, VOC).

    Features:
        - Stateless saving interface (works without manual creation of AnnotationFile object).
        - Format-specific save functions (save_labelme, save_coco, save_voc).
        - Optional file backup on overwrite.

    Usage examples:
        save(shapes, 'file.json', 'labelme')
        save_labelme(shapes, 'labelme.json')
        save_coco(shapes, 'coco.json')
"""

__all__ = ['save', 'save_labelme', 'save_coco', 'save_voc']

from pathlib import Path
from typing import Union, Tuple

from ..core.annotation_file import AnnotationFile
from ..public_enums import Adapters
from ..shape import Shape


def save(
        shapes: Tuple[Shape, ...],
        file_path: Union[str, Path],
        markup_type: str | Adapters,
        backup: bool = True) -> None:
    """
        Save a tuple of Shape objects to an annotation file using the specified format.
        Stateless: for use when you don't have a saved AnnotationFile object.
        Args:
            shapes: Tuple of Shape objects to save.
            file_path: Path to save the annotation file.
            markup_type: Markup type as a string or Adapters enum.
            backup: If True, creates a backup before overwrite (default: True).
        Raises:
            ValueError: If neither file_path nor markup_type are provided or cannot be resolved.
    """
    if not file_path:
        raise ValueError("file_path must be provided for stateless save().")
    if not markup_type:
        raise ValueError("markup_type must be provided for stateless save().")
    AnnotationFile(file_path, markup_type, keep_json=True, validate_file=False).save(shapes, backup=backup)


def save_labelme(shapes: Tuple[Shape, ...], file_path: Union[str, Path], backup: bool = False) -> None:
    """Save shapes in LabelMe format."""
    save(shapes, file_path, Adapters.labelme, backup)


def save_coco(shapes: Tuple[Shape, ...], file_path: Union[str, Path], backup: bool = False) -> None:
    """Save shapes in COCO format."""
    save(shapes, file_path, Adapters.coco, backup)


def save_voc(shapes: Tuple[Shape, ...], file_path: Union[str, Path], backup: bool = False) -> None:
    """Save shapes in VOC format."""
    save(shapes, file_path, Adapters.voc, backup)
