"""
    Annotation Parser Public API
    ===========================

    Unified interface for parsing annotation files from different markup tools (LabelMe, COCO, VOC, ...).

    Provides simple functions for:
        - Listing available adapters.
        - Creating an annotation parser object for a given file and markup type.
        - Parsing annotations and returning normalized Shape objects.
        - Parsing specific formats via one-line functions: parse_labelme, parse_coco, parse_voc.
        - Saving a tuple of Shape objects to file in any supported format (universal and format-specific).

    Usage examples:
        adapters = available_adapters()
        shapes = parse('annotations.json', 'labelme')
        shapes = parse_labelme('annotations.json')
        parser = create('annotations.json', 'labelme')
        shapes = parser.parse()
        save(shapes, 'new.json', 'labelme')
        save_labelme(shapes, 'labelme.json')
"""

__all__ = [
    'Adapters', 'available_adapters', 'create',
    'parse', 'parse_labelme', 'parse_coco', 'parse_voc',
    'save', 'save_labelme', 'save_coco', 'save_voc'
]

from pathlib import Path
from typing import Any, Optional, Union, Tuple

from .core.annotation_file import AnnotationFile
from .adapters import AdapterFactory
from .public_enums import Adapters
from .shape import Shape


def available_adapters() -> list[str]:
    """
        Returns a list of all currently registered adapters,
        including plugins and user-defined ones.
    """
    return AdapterFactory.list_adapters()


def create(
        file_path: Union[str, Path],
        markup_type: str | Adapters,
        shift_point: Optional[Any] = None) -> AnnotationFile:
    """
        Create an annotation parser object for the given file and markup type.
        Args:
            file_path: Path to the annotation file.
            markup_type: Markup type as a string ('labelme', 'coco', 'voc') or Adapters enum.
            shift_point: Optional function or coordinates for shifting points during parsing.
        Returns:
            AnnotationFile: Parser instance ready to parse shapes.
    """
    return AnnotationFile(file_path, markup_type, keep_json=True, shift_point=shift_point)


def parse(
        file_path: Union[str, Path],
        markup_type: str | Adapters,
        shift_point: Optional[Any] = None) -> Tuple[Shape, ...]:
    """
        Parse the annotation file and return a tuple of Shape objects.
        Args:
            file_path: Path to the annotation file.
            markup_type: Markup type as a string ('labelme', 'coco', 'voc') or Adapters enum.
            shift_point: Optional function or coordinates for shifting points during parsing.
        Returns:
            Tuple[Shape, ...]: Tuple of parsed and normalized shapes.
    """
    return AnnotationFile(file_path, markup_type, keep_json=True, shift_point=shift_point).parse()


def parse_labelme(file_path: Union[str, Path], shift_point: Optional[Any] = None) -> Tuple[Shape, ...]:
    """
        Parse a LabelMe annotation file and return a tuple of Shape objects.
        Args:
            file_path: Path to the LabelMe annotation file.
            shift_point: Optional function or coordinates for shifting points during parsing.
        Returns:
            Tuple[Shape, ...]: Tuple of parsed and normalized shapes.
    """
    return parse(file_path, Adapters.labelme, shift_point=shift_point)


def parse_coco(file_path: Union[str, Path], shift_point: Optional[Any] = None) -> Tuple[Shape, ...]:
    """
        Parse a COCO annotation file and return a tuple of Shape objects.
        Args:
            file_path: Path to the COCO annotation file.
            shift_point: Optional function or coordinates for shifting points during parsing.
        Returns:
            Tuple[Shape, ...]: Tuple of parsed and normalized shapes.
    """
    return parse(file_path, Adapters.coco, shift_point=shift_point)


def parse_voc(file_path: Union[str, Path], shift_point: Optional[Any] = None) -> Tuple[Shape, ...]:
    """
        Parse a VOC annotation file and return a tuple of Shape objects.
        Args:
            file_path: Path to the VOC annotation file.
            shift_point: Optional function or coordinates for shifting points during parsing.
        Returns:
            Tuple[Shape, ...]: Tuple of parsed and normalized shapes.
    """
    return parse(file_path, Adapters.voc, shift_point=shift_point)


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
