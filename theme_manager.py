#!/usr/bin/env python3
"""Install, activate, inspect, and restore the Calibre Clarity theme."""

import argparse
import datetime as dt
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import time
from pathlib import Path


BUNDLE_DIR = Path(__file__).resolve().parent
PROFILE_PATH = BUNDLE_DIR / "profile.json"
ICON_DIR = BUNDLE_DIR / "icon-theme-png"
DETAILS_DIR = BUNDLE_DIR / "book-details"
NATIVE_ARCHIVE = BUNDLE_DIR / "calibre-clarity-icon-theme.zip"
BUILDER = BUNDLE_DIR / "build_native_theme.py"
STATE_FILENAME = "calibre-clarity-theme-state.json"
MISSING = {"exists": False}


def default_config_dir():
    configured = os.environ.get("CALIBRE_CONFIG_DIRECTORY")
    if configured:
        return Path(configured).expanduser().resolve()
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Preferences" / "calibre"
    if os.name == "nt":
        return Path(os.environ["APPDATA"]) / "calibre"
    return Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "calibre"


def calibre_debug_path():
    configured = os.environ.get("CALIBRE_DEBUG")
    candidates = [
        configured,
        "/Applications/calibre.app/Contents/MacOS/calibre-debug",
        shutil.which("calibre-debug"),
    ]
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return Path(candidate)
    raise SystemExit("calibre-debug is required. Install calibre or set CALIBRE_DEBUG.")


def read_json(path, default=None):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {} if default is None else default


def write_json_atomic(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)


def calibre_is_running():
    if sys.platform == "darwin":
        result = subprocess.run(
            ["pgrep", "-x", "calibre"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        return result.returncode == 0
    return False


def require_calibre_stopped():
    if calibre_is_running():
        raise SystemExit(
            "Fermez calibre avant d'activer ou de restaurer le theme, puis relancez la commande."
        )


def launch_calibre():
    if sys.platform == "darwin":
        subprocess.Popen(["open", "-a", "calibre"])
        return
    executable = shutil.which("calibre")
    if executable:
        subprocess.Popen([executable])


def snapshot_value(mapping, key):
    return {"exists": True, "value": mapping[key]} if key in mapping else MISSING.copy()


def restore_value(mapping, key, snapshot):
    if snapshot.get("exists"):
        mapping[key] = snapshot.get("value")
    else:
        mapping.pop(key, None)


def known_libraries(gui_preferences, explicit_libraries):
    paths = set()
    usage = gui_preferences.get("library_usage_stats", {})
    if isinstance(usage, dict):
        paths.update(usage)
    paths.update(str(Path(x).expanduser().resolve()) for x in explicit_libraries)
    return [Path(x) for x in sorted(paths) if (Path(x) / "metadata.db").is_file()]


def read_library_preferences(database, keys):
    answer = {}
    with sqlite3.connect(database) as connection:
        for key in keys:
            row = connection.execute("SELECT val FROM preferences WHERE key = ?", (key,)).fetchone()
            answer[key] = {"exists": bool(row), "value": row[0] if row else None}
    return answer


def write_library_preferences(database, values):
    with sqlite3.connect(database) as connection:
        for key, value in values.items():
            serialized = json.dumps(value, ensure_ascii=False, indent=2)
            connection.execute(
                "INSERT INTO preferences(key, val) VALUES(?, ?) "
                "ON CONFLICT(key) DO UPDATE SET val = excluded.val",
                (key, serialized),
            )


def restore_library_preferences(database, snapshots):
    if not database.is_file():
        return
    with sqlite3.connect(database) as connection:
        for key, snapshot in snapshots.items():
            if snapshot.get("exists"):
                connection.execute(
                    "INSERT INTO preferences(key, val) VALUES(?, ?) "
                    "ON CONFLICT(key) DO UPDATE SET val = excluded.val",
                    (key, snapshot["value"]),
                )
            else:
                connection.execute("DELETE FROM preferences WHERE key = ?", (key,))


def copy_details_resources(config_dir):
    destination = config_dir / "resources" / "templates"
    destination.mkdir(parents=True, exist_ok=True)
    template_uri = destination.resolve().as_uri()
    for source in DETAILS_DIR.iterdir():
        if not source.is_file():
            continue
        target = destination / source.name
        if source.name == "book_details.css":
            css = source.read_text(encoding="utf-8")
            css = css.replace("__CALIBRE_TEMPLATES_URI__", template_uri)
            target.write_text(css, encoding="utf-8")
        else:
            shutil.copy2(source, target)


def install_native_icon_theme(config_dir):
    env = os.environ.copy()
    env["CALIBRE_CONFIG_DIRECTORY"] = str(config_dir)
    env.setdefault("QT_QPA_PLATFORM", "offscreen")
    command = [
        str(calibre_debug_path()),
        "-e",
        str(BUILDER),
        "--",
        str(ICON_DIR),
        str(NATIVE_ARCHIVE),
        "--install",
    ]
    subprocess.run(command, check=True, env=env)


def make_backup(config_dir, profile, libraries):
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_dir = config_dir / "backups" / "calibre-clarity-selectable" / stamp
    backup_dir.mkdir(parents=True)

    gui_path = config_dir / "gui.json"
    gui = read_json(gui_path)
    state = {
        "active": False,
        "created_at": dt.datetime.now().isoformat(timespec="seconds"),
        "backup_dir": str(backup_dir),
        "gui_preferences": {
            key: snapshot_value(gui, key) for key in profile["gui_preferences"]
        },
        "libraries": {},
        "resources": {},
    }

    images = config_dir / "resources" / "images"
    state["resources"]["images_existed"] = images.exists()
    if images.exists():
        shutil.copytree(images, backup_dir / "images")

    templates = config_dir / "resources" / "templates"
    template_backup = backup_dir / "templates"
    for source in DETAILS_DIR.iterdir():
        if not source.is_file():
            continue
        target = templates / source.name
        existed = target.is_file()
        state["resources"].setdefault("template_files", {})[source.name] = existed
        if existed:
            template_backup.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target, template_backup / source.name)

    palette = profile["icon_palette"]
    rcc = config_dir / f"icons-{palette}.rcc"
    state["resources"]["rcc_existed"] = rcc.is_file()
    state["resources"]["rcc_name"] = rcc.name
    if rcc.is_file():
        shutil.copy2(rcc, backup_dir / rcc.name)

    library_keys = profile["library_preferences"].keys()
    for library in libraries:
        database = library / "metadata.db"
        state["libraries"][str(library)] = read_library_preferences(database, library_keys)

    write_json_atomic(config_dir / STATE_FILENAME, state)
    return state


def apply_profile(config_dir, profile, explicit_libraries):
    gui_path = config_dir / "gui.json"
    gui = read_json(gui_path)
    libraries = known_libraries(gui, explicit_libraries)
    state_path = config_dir / STATE_FILENAME
    existing_state = read_json(state_path, default={})
    if existing_state.get("active"):
        state = existing_state
    else:
        state = make_backup(config_dir, profile, libraries)

    images = config_dir / "resources" / "images"
    if images.exists() and not existing_state.get("active"):
        shutil.rmtree(images)
    images.mkdir(parents=True, exist_ok=True)

    gui.update(profile["gui_preferences"])
    write_json_atomic(gui_path, gui)
    copy_details_resources(config_dir)
    install_native_icon_theme(config_dir)

    for library in libraries:
        write_library_preferences(
            library / "metadata.db", profile["library_preferences"]
        )

    state["active"] = True
    state["activated_at"] = dt.datetime.now().isoformat(timespec="seconds")
    write_json_atomic(state_path, state)
    print(f"Theme active: {profile['name']}")
    print(f"Configuration: {config_dir}")
    print(f"Bibliotheques configurees: {len(libraries)}")


def restore_profile(config_dir):
    state_path = config_dir / STATE_FILENAME
    state = read_json(state_path, default={})
    if not state.get("active"):
        raise SystemExit("Le theme Calibre Clarity n'est pas actif.")
    backup_dir = Path(state["backup_dir"])

    gui_path = config_dir / "gui.json"
    gui = read_json(gui_path)
    for key, snapshot in state["gui_preferences"].items():
        restore_value(gui, key, snapshot)
    write_json_atomic(gui_path, gui)

    images = config_dir / "resources" / "images"
    if images.exists():
        active_extra = backup_dir / "images-added-while-active"
        if any(images.iterdir()):
            shutil.copytree(images, active_extra, dirs_exist_ok=True)
        shutil.rmtree(images)
    if state["resources"].get("images_existed"):
        shutil.copytree(backup_dir / "images", images)

    templates = config_dir / "resources" / "templates"
    template_backup = backup_dir / "templates"
    for name, existed in state["resources"].get("template_files", {}).items():
        target = templates / name
        if existed:
            shutil.copy2(template_backup / name, target)
        elif target.exists():
            target.unlink()

    rcc = config_dir / state["resources"]["rcc_name"]
    if state["resources"].get("rcc_existed"):
        shutil.copy2(backup_dir / rcc.name, rcc)
    elif rcc.exists():
        rcc.unlink()

    for library_path, snapshots in state.get("libraries", {}).items():
        restore_library_preferences(Path(library_path) / "metadata.db", snapshots)

    state["active"] = False
    state["restored_at"] = dt.datetime.now().isoformat(timespec="seconds")
    write_json_atomic(state_path, state)
    print("Configuration precedente restauree.")
    print(f"Sauvegarde conservee: {backup_dir}")


def build_theme(config_dir):
    env = os.environ.copy()
    env["CALIBRE_CONFIG_DIRECTORY"] = str(config_dir)
    env.setdefault("QT_QPA_PLATFORM", "offscreen")
    command = [
        str(calibre_debug_path()),
        "-e",
        str(BUILDER),
        "--",
        str(ICON_DIR),
        str(NATIVE_ARCHIVE),
    ]
    subprocess.run(command, check=True, env=env)


def show_status(config_dir):
    state = read_json(config_dir / STATE_FILENAME, default={})
    metadata = read_json(ICON_DIR / "metadata.json")
    print(f"Theme: {metadata.get('title', 'Calibre Clarity')}")
    print(f"Etat: {'actif' if state.get('active') else 'inactif'}")
    print(f"Archive native: {NATIVE_ARCHIVE}")
    print(f"Archive presente: {'oui' if NATIVE_ARCHIVE.is_file() else 'non'}")


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("activate", "restore", "build", "status"))
    parser.add_argument("--config-dir", type=Path, default=default_config_dir())
    parser.add_argument("--library", action="append", default=[])
    parser.add_argument("--launch", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    config_dir = args.config_dir.expanduser().resolve()
    profile = read_json(PROFILE_PATH)

    if args.command == "status":
        show_status(config_dir)
        return
    if args.command == "build":
        build_theme(config_dir)
        return

    require_calibre_stopped()
    if args.command == "activate":
        apply_profile(config_dir, profile, args.library)
    else:
        restore_profile(config_dir)
    if args.launch:
        time.sleep(0.5)
        launch_calibre()


if __name__ == "__main__":
    main()
