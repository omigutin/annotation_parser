"""
    High-Level Annotation Parsing API
    ================================================

    This module provides top-level functions for reading and parsing annotation files
    (LabelMe, COCO, VOC, ...), returning normalized Shape objects.

    Features:
        - Parse annotation files by format or path.
        - Format-specific one-line parsing (LabelMe, COCO, VOC).
        - Optional shift_point for coordinate normalization.

    Example usage:
        shapes = parse('file.json', 'labelme')
        shapes = parse_labelme('file.json')
        shapes = parse_coco('file.json')
"""

__all__ = ['parse', 'parse_labelme', 'parse_coco', 'parse_voc']

from pathlib import Path
from typing import Union, Tuple

from ..core.annotation_file import AnnotationFile
from ..public_enums import Adapters
from ..shape import Shape
from ..types import ShiftPointType


def parse(
        file_path: Union[str, Path],
        markup_type: str | Adapters,
        shift_point: ShiftPointType = None) -> Tuple[Shape, ...]:
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


def parse_labelme(file_path: Union[str, Path], shift_point: ShiftPointType = None) -> Tuple[Shape, ...]:
    """
        Parse a LabelMe annotation file and return a tuple of Shape objects.
        Args:
            file_path: Path to the LabelMe annotation file.
            shift_point: Optional function or coordinates for shifting points during parsing.
        Returns:
            Tuple[Shape, ...]: Tuple of parsed and normalized shapes.
    """
    return parse(file_path, Adapters.labelme, shift_point=shift_point)


def parse_coco(file_path: Union[str, Path], shift_point: ShiftPointType = None) -> Tuple[Shape, ...]:
    """
        Parse a COCO annotation file and return a tuple of Shape objects.
        Args:
            file_path: Path to the COCO annotation file.
            shift_point: Optional function or coordinates for shifting points during parsing.
        Returns:
            Tuple[Shape, ...]: Tuple of parsed and normalized shapes.
    """
    return parse(file_path, Adapters.coco, shift_point=shift_point)


def parse_voc(file_path: Union[str, Path], shift_point: ShiftPointType = None) -> Tuple[Shape, ...]:
    """
        Parse a VOC annotation file and return a tuple of Shape objects.
        Args:
            file_path: Path to the VOC annotation file.
            shift_point: Optional function or coordinates for shifting points during parsing.
        Returns:
            Tuple[Shape, ...]: Tuple of parsed and normalized shapes.
    """
    return parse(file_path, Adapters.voc, shift_point=shift_point)
