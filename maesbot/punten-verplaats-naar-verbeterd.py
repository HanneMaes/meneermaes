#!/usr/bin/env python3
"""
move.py - move files or directories into the "Taken en toetsen Verbeterd" folder.

Usage:
    python3 move.py file-or-dir [file-or-dir ...]

You are asked for:
  1. a directory inside the destination: pick a number, or type a new name
  2. an optional directory inside that one: type a name to create it, or
     press Enter to put everything directly in the directory from step 1

Afterwards the destination is listed with ls, so you can see everything
arrived.
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

# Built from the home directory of whoever runs the script (no hard-coded
# /home/hanne).
BASE_DIR = (
    Path.home()
    / "Documents"
    / "Nextcloud"
    / "School"
    / "Automatisatie"
    / "maesbot-private-data"
    / "Punten"
    / "Taken en toetsen Verbeterd"
)

if sys.stdout.isatty():
    GREEN, RED, DIM, NC = "\033[0;32m", "\033[0;31m", "\033[2m", "\033[0m"
else:
    GREEN = RED = DIM = NC = ""


#############################################################################
# Helpers


def list_subdirs(parent):
    """Names of the visible directories directly inside parent, sorted."""

    if not parent.is_dir():
        return []

    return sorted(
        (
            path.name
            for path in parent.iterdir()
            if path.is_dir() and not path.name.startswith(".")
        ),
        key=str.lower,
    )


def clean_name(raw):
    """Return a usable single directory name, or None when it isn't one."""

    name = raw.strip()

    if not name or "/" in name or name in (".", ".."):
        return None

    return name


def find_existing(name, existing):
    """
    Return the existing directory that matches name, ignoring upper/lower
    case.

    This stops "5ad - hardware" from becoming a second folder next to
    "5AD - hardware", which Nextcloud on Windows would see as a clash.
    """

    for candidate in existing:
        if candidate.lower() == name.lower():
            return candidate

    return None


#############################################################################
# The two questions


def choose_directory(base):
    """Step 1: pick an existing directory by number, or type a new name."""

    existing = list_subdirs(base)

    print(f"\nDestination: {base}\n")

    if existing:
        for number, name in enumerate(existing, start=1):
            print(f"  {number:>2}) {name}")
    else:
        print("  (no directories yet)")

    while True:
        answer = input("\nPick a number, or type a new directory name: ").strip()

        if not answer:
            continue

        if answer.isdigit():
            number = int(answer)

            if 1 <= number <= len(existing):
                return existing[number - 1]

            print(f"{RED}There is no option {number}.{NC}")
            continue

        name = clean_name(answer)

        if name is None:
            print(f"{RED}That is not a valid directory name (no '/').{NC}")
            continue

        match = find_existing(name, existing)

        if match:
            print(f"{DIM}Using the existing directory '{match}'.{NC}")
            return match

        return name


def ask_subdirectory(parent, parent_name):
    """
    Step 2: type a directory to create inside the chosen one, or press Enter
    to skip. Returns None when skipped.
    """

    existing = list_subdirs(parent)

    while True:
        answer = input(
            f"\nNew directory inside '{parent_name}' "
            f"(press Enter to use '{parent_name}' itself): "
        ).strip()

        if not answer:
            return None

        name = clean_name(answer)

        if name is None:
            print(f"{RED}That is not a valid directory name (no '/').{NC}")
            continue

        match = find_existing(name, existing)

        if match:
            print(f"{DIM}Using the existing directory '{match}'.{NC}")
            return match

        return name


#############################################################################
# Main


def main():
    parser = argparse.ArgumentParser(
        description='Move files or directories into "Taken en toetsen Verbeterd".'
    )
    parser.add_argument(
        "sources",
        nargs="+",
        metavar="file-or-dir",
        help="one or more files or directories to move",
    )
    args = parser.parse_args()

    # abspath tidies "." / ".." / trailing slashes without following
    # symlinks, so a symlink is moved as a symlink.
    sources = [Path(os.path.abspath(os.path.expanduser(s))) for s in args.sources]

    missing = [s for s in sources if not (s.exists() or s.is_symlink())]

    if missing:
        for source in missing:
            print(f"{RED}✗ Not found: {source}{NC}")

        sys.exit(1)

    if not BASE_DIR.is_dir():
        print(f"{RED}✗ Destination folder does not exist: {BASE_DIR}{NC}")

        sys.exit(1)

    #########################################################################
    # Ask where to put it. Nothing is created until both questions are
    # answered, so pressing Ctrl+C leaves everything untouched.

    try:
        first = choose_directory(BASE_DIR)
        second = ask_subdirectory(BASE_DIR / first, first)

    except (KeyboardInterrupt, EOFError):
        print("\nAborted, nothing was moved.")

        sys.exit(1)

    destination = BASE_DIR / first

    if second:
        destination = destination / second

    #########################################################################
    # Move

    is_new = not destination.exists()

    destination.mkdir(parents=True, exist_ok=True)

    print(
        f"\nMoving {len(sources)} item(s) to {destination}"
        + (" (new directory)" if is_new else "")
    )

    failures = 0

    for source in sources:
        target = destination / source.name

        if target.exists() or target.is_symlink():
            print(
                f"{RED}✗ {source.name}: already exists in the destination, skipped{NC}"
            )
            failures += 1
            continue

        try:
            shutil.move(str(source), str(destination))

        except (shutil.Error, OSError) as error:
            print(f"{RED}✗ {source}: {error}{NC}")
            failures += 1
            continue

        print(f"{GREEN}✓ Moved{NC} {source}")

    #########################################################################
    # ls the destination so you can see they arrived

    print(f"\n{DIM}$ ls -lh {destination}{NC}")

    try:
        subprocess.run(
            ["ls", "-lh", "--color=auto", str(destination)],
            check=False,
        )

    except FileNotFoundError:
        for entry in sorted(destination.iterdir()):
            print(entry.name)

    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
