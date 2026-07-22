#!/usr/bin/env python3
"""
Scans the walkxcode/dashboard-icons repo folders (png/, svg/, webp/)
and generates icons.json — a manifest of every icon and which
formats it's available in.

Usage:
    Place this script in the ROOT of your forked dashboard-icons repo
    (same level as the png/, svg/, webp/ folders) and run:

        python3 generate_manifest.py

    This will create/overwrite icons.json in the same folder.
"""

import json
import os

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
FORMAT_FOLDERS = ["png", "svg", "webp"]
OUTPUT_FILE = os.path.join(REPO_ROOT, "icons.json")


def scan_icons():
    icons = {}

    for fmt in FORMAT_FOLDERS:
        folder_path = os.path.join(REPO_ROOT, fmt)
        if not os.path.isdir(folder_path):
            print(f"  Skipping '{fmt}/' (not found)")
            continue

        count = 0
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if not os.path.isfile(file_path):
                continue

            name, ext = os.path.splitext(filename)
            ext = ext.lower().lstrip(".")
            if ext != fmt:
                continue

            if name not in icons:
                icons[name] = {"name": name, "formats": []}
            icons[name]["formats"].append(fmt)
            count += 1

        print(f"  Found {count} files in '{fmt}/'")

    # Convert dict to sorted list
    icon_list = sorted(icons.values(), key=lambda x: x["name"])
    for icon in icon_list:
        icon["formats"].sort()

    return icon_list


def main():
    print("Scanning dashboard-icons repo...")
    icon_list = scan_icons()

    manifest = {
        "generated_count": len(icon_list),
        "icons": icon_list,
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"\nDone. Wrote {len(icon_list)} icons to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
