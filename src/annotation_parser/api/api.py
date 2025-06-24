"""
    API for Adapter Listing and Parser Creation
    ===========================================

    This module provides entry points for:
        - Listing all available annotation adapters (including user extensions).
        - Creating an annotation parser (AnnotationFile) for a specific file and markup type.

    Typical usage:
        adapters = available_adapters()
        parser = create('annotations.json', 'labelme')
        shapes = parser.parse()
"""


__all__ = ['available_adapters', 'create']

from pathlib import Path
from typing import Union

from ..core.annotation_file import AnnotationFile
from ..adapters import AdapterFactory
from ..public_enums import Adapters
from ..types import ShiftPointType


def available_adapters() -> list[str]:
    """
        Returns a list of all currently registered adapters,
        including plugins and user-defined ones.
    """
    return AdapterFactory.list_adapters()


def create(
        file_path: Union[str, Path],
        markup_type: str | Adapters,
        shift_point: ShiftPointType = None) -> AnnotationFile:
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
