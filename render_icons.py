#!/usr/bin/env python3
"""Render editable SVG artwork to genuine PNG files using calibre's Qt runtime."""

import argparse
import os
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image
from qt.core import QApplication, QByteArray, QImage, QPainter, QSvgRenderer


ROOT = Path(__file__).resolve().parent
SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)
NORMALIZED = "data-clarity-menu-readability"


def render(data, size=128):
    renderer = QSvgRenderer(QByteArray(data))
    if not renderer.isValid():
        raise ValueError("Invalid SVG")
    image = QImage(size, size, QImage.Format.Format_RGBA8888)
    image.fill(0)
    painter = QPainter(image)
    try:
        renderer.render(painter)
    finally:
        painter.end()
    return image


def ink_bounds(image):
    rgba = image.convertToFormat(QImage.Format.Format_RGBA8888)
    raw = rgba.constBits().asstring(rgba.sizeInBytes())
    pixels = Image.frombytes("RGBA", (rgba.width(), rgba.height()), raw)
    return pixels.getchannel("A").point(lambda a: 255 if a >= 24 else 0).getbbox()


def normalize(data, dark=False):
    root = ET.fromstring(data)
    if root.get(NORMALIZED):
        return data
    if root.get("viewBox") != "0 0 128 128":
        raise ValueError("Expected the theme's 128 by 128 viewBox")
    for node in root.iter():
        for attr in ("stroke", "fill"):
            if not dark and node.get(attr, "").lower() == "#8e8e93":
                node.set(attr, "#636366")

    bounds = ink_bounds(render(ET.tostring(root), 512))
    if bounds is None:
        return data
    left, top, right, bottom = (value / 4 for value in bounds)
    # Target 14 visible pixels in a 16px menu slot; retain a 1px clear edge.
    scale = max(1.0, 112 / max(right - left, bottom - top))
    if scale > 1.001:
        group = ET.Element(f"{{{SVG_NS}}}g", {
            "transform": (
                f"translate(64 64) scale({scale:.6f}) "
                f"translate({-(left + right) / 2:.4f} {-(top + bottom) / 2:.4f})"
            ),
        })
        for child in list(root):
            root.remove(child)
            group.append(child)
        root.append(group)
    root.set(NORMALIZED, "1")
    ET.indent(root, space="  ")
    return ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--normalize", action="store_true",
                        help="Normalize SVG margins and neutral contrast once, in place")
    args = parser.parse_args()
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    app = QApplication.instance() or QApplication([])
    count = 0
    for source in sorted((ROOT / "icon-sources-svg").rglob("*.svg")):
        data = source.read_bytes()
        if args.normalize:
            updated = normalize(data, dark="-for-dark-theme" in source.name)
            if updated != data:
                source.write_bytes(updated)
            data = updated
        target = ROOT / "icon-theme-png" / source.relative_to(ROOT / "icon-sources-svg")
        target = target.with_suffix(".png")
        target.parent.mkdir(parents=True, exist_ok=True)
        if not render(data).save(str(target), "PNG"):
            raise OSError(f"Could not save {target}")
        count += 1
    print(f"Rendered {count} SVG sources to PNG using Qt {app.platformName()}")


if __name__ == "__main__":
    main()
