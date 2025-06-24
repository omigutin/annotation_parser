#!/usr/bin/env python3
"""
CLI for AnnotationParser
========================

Позволяет парсить, сохранять, фильтровать аннотации через командную строку.
Все функции можно вызывать по отдельности.
"""

import argparse
from pathlib import Path
import sys

from ..annotation_parser import create, parse_labelme, save_labelme
from ..annotation_parser.api.shapes_api import (
    filter_shapes,
    get_shapes_by_label,
)
from ..annotation_parser.public_enums import ShapeType


def main():
    parser = argparse.ArgumentParser(
        description="AnnotationParser CLI: parse, save, filter annotation files."
    )
    subparsers = parser.add_subparsers(dest='command', required=True)

    # parse
    parse_p = subparsers.add_parser("parse", help="Parse annotation file")
    parse_p.add_argument("--file", required=True, help="Path to annotation file")
    parse_p.add_argument("--adapter", required=True, help="Adapter name (labelme, coco, etc.)")

    # save
    save_p = subparsers.add_parser("save", help="Save shapes to annotation file")
    save_p.add_argument("--file", required=True, help="Path to annotation file to parse")
    save_p.add_argument("--adapter", required=True, help="Adapter name")
    save_p.add_argument("--out", required=True, help="Path to output file")
    save_p.add_argument("--backup", action="store_true", help="Save backup .bak file")

    # filter
    filter_p = subparsers.add_parser("filter", help="Filter shapes by label or other predicate")
    filter_p.add_argument("--file", required=True, help="Path to annotation file to parse")
    filter_p.add_argument("--adapter", required=True, help="Adapter name")
    filter_p.add_argument("--label", help="Filter by label")
    filter_p.add_argument("--number", type=int, help="Filter by number")
    filter_p.add_argument("--wz_number", type=int, help="Filter by working zone number (wz_number)")

    args = parser.parse_args()

    if args.command == "parse":
        do_parse(args)
    elif args.command == "save":
        do_save(args)
    elif args.command == "filter":
        do_filter(args)
    else:
        parser.print_help()


def do_parse(args):
    file = Path(args.file)
    try:
        parser = create(file, args.adapter)
        shapes = parser.parse()
        print(f"Parsed {len(shapes)} shapes:")
        for shape in shapes:
            print(shape)
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)


def do_save(args):
    file = Path(args.file)
    out_file = Path(args.out)
    try:
        parser = create(file, args.adapter)
        shapes = parser.parse()
        save_labelme(shapes, out_file, backup=args.backup)
        print(f"Saved {len(shapes)} shapes to '{out_file}'. Backup: {args.backup}")
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)


def do_filter(args):
    file = Path(args.file)
    try:
        parser = create(file, args.adapter)
        shapes = parser.parse()
        filtered = shapes
        # Логика фильтрации
        if args.label:
            filtered = get_shapes_by_label(filtered, args.label)
        if args.number is not None:
            # Применяем фильтрацию по номеру (custom predicate)
            filtered = tuple(s for s in filtered if getattr(s, "number", None) == args.number)
        if args.wz_number is not None:
            filtered = tuple(s for s in filtered if getattr(s, "wz_number", None) == args.wz_number)
        print(f"Filtered shapes ({len(filtered)}):")
        for shape in filtered:
            print(shape)
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
