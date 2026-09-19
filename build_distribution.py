#!/usr/bin/env python3
"""Build the optional manual UX pack and a MobileRead submission folder."""

import argparse
import base64
import hashlib
import json
import re
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RESOURCE = re.compile(r'url\("__CALIBRE_TEMPLATES_URI__/([^"/]+\.svg)"\)')


def portable_css():
    source = ROOT / "book-details"
    css = (source / "book_details.css").read_text(encoding="utf-8")

    def embed(match):
        image = (source / match.group(1)).read_bytes()
        encoded = base64.b64encode(image).decode("ascii")
        return f'url("data:image/svg+xml;base64,{encoded}")'

    css = RESOURCE.sub(embed, css)
    if "__CALIBRE_TEMPLATES_URI__" in css:
        raise ValueError("Unresolved CSS resource")
    return (
        "/* Generated from book-details/*. SVG artwork: CC BY 4.0; CSS: MIT.\n"
        "   Attribution: Loic Gridaine, https://github.com/gridaine/calibre-clarity */\n"
        + css
    ).encode("utf-8")


def build(output, icon_archive):
    with zipfile.ZipFile(icon_archive) as archive:
        metadata = json.loads(archive.read("calibre_clarity/metadata.json"))
        if metadata["name"] != "calibre_clarity":
            raise ValueError("Expected a Calibre Clarity native icon archive")
        preview = archive.read("calibre_clarity/icon-theme-cover.jpg")
    output.mkdir(parents=True, exist_ok=True)
    native = output / "calibre-clarity-icon-theme.zip"
    if native.resolve() != icon_archive.resolve():
        shutil.copy2(icon_archive, native)
    (output / "calibre-clarity-icons-preview.jpg").write_bytes(preview)

    ux = output / "calibre-clarity-ux.zip"
    files = {
        "book_details.css": portable_css(),
        "README.fr.md": (ROOT / "docs/OPTIONAL_UX.fr.md").read_bytes(),
        "README.md": (ROOT / "docs/OPTIONAL_UX.md").read_bytes(),
        "LICENSE": (ROOT / "LICENSE").read_bytes(),
        "LICENSE-ASSETS.md": (ROOT / "LICENSE-ASSETS.md").read_bytes(),
    }
    # Fixed ZIP timestamps keep identical sources reproducible across builds.
    with zipfile.ZipFile(ux, "w") as archive:
        for name, data in files.items():
            info = zipfile.ZipInfo("calibre-clarity-ux/" + name, (2020, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)

    for source, name in (
        ("docs/MOBILEREAD.fr.md", "LIRE-AVANT-SOUMISSION.md"),
        ("docs/mobileread-post.txt", "mobileread-post.txt"),
    ):
        shutil.copy2(ROOT / source, output / name)
    checksums = "".join(
        f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n"
        for path in (native, ux)
    )
    (output / "SHA256SUMS.txt").write_text(checksums, encoding="ascii")
    return {"icon_theme": str(native), "optional_ux": str(ux),
            "submission": str(output), "icon_revision": metadata["version"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--icon-archive", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "dist/submission")
    args = parser.parse_args()
    print(json.dumps(build(args.output_dir, args.icon_archive), indent=2))


if __name__ == "__main__":
    main()
