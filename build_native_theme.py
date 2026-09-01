#!/usr/bin/env python3
"""Build and optionally install the native calibre icon-theme archive."""

import argparse
import json
import os
from pathlib import Path

from calibre.gui2 import icon_resource_manager
from calibre.gui2.icon_theme import (
    create_themeball,
    install_icon_theme,
    read_theme_from_folder,
    verify_theme,
)
from qt.core import QApplication


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("icon_dir", type=Path)
    parser.add_argument("output_zip", type=Path)
    parser.add_argument("--install", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    app = QApplication.instance() or QApplication([])
    del app

    report = read_theme_from_folder(str(args.icon_dir))
    if verify_theme(report):
        details = "\n".join(f"{name}: {error}" for name, error in report.bad.items())
        raise SystemExit(f"Invalid icon files:\n{details}")

    metadata_path = args.icon_dir / "metadata.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    metadata.setdefault("name", report.name)
    metadata.setdefault("color_palette", "light")
    metadata_path.write_text(
        json.dumps(metadata, ensure_ascii=True, indent=2) + "\n", encoding="utf-8"
    )

    raw, prefix, icon_zip_data = create_themeball(report, metadata)
    args.output_zip.parent.mkdir(parents=True, exist_ok=True)
    args.output_zip.write_bytes(raw)

    if args.install:
        palette = metadata["color_palette"]
        rcc_path = icon_resource_manager.user_theme_resource_file(palette)
        install_icon_theme(metadata, icon_zip_data, rcc_path, palette)

    print(
        json.dumps(
            {
                "archive": str(args.output_zip),
                "installed": args.install,
                "name": metadata["name"],
                "palette": metadata["color_palette"],
                "prefix": prefix,
                "icons": report.number,
                "missing_core_icons": len(report.missing),
                "extra_icons": len(report.extra),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
