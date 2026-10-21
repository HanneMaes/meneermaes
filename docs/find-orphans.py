#!/usr/bin/env python3
""" """

import argparse
import fnmatch
import os
import re
import sys
from collections import defaultdict
from urllib.parse import unquote

SKIP_DIRS = {
    ".git",
    "node_modules",
    "vendor",
    "_site",
    ".jekyll-cache",
    ".sass-cache",
    ".bundle",
}
PAGE_EXT = (".md", ".markdown", ".html", ".htm")
MAX_SIZE = 10 * 1024 * 1024

SPLIT = re.compile(r"""[\s()\[\]<>"'=,;{}|]+""")
LINK_RES = [
    re.compile(r"\]\(\s*<?([^)\s>]+)"),  # [x](url)
    re.compile(r"^[ ]{0,3}\[[^\]]+\]:\s*<?(\S+?)>?(?:\s|$)", re.M),  # [x]: url
    re.compile(r"""\b(?:href|src)\s*=\s*["']([^"']+)["']""", re.I),  # <a href>
    re.compile(r"""\{%-?\s*(?:link|post_url)\s+['"]?([^\s'"%]+)"""),  # {% link %}
]


def clean(tok):
    tok = re.sub(r"[?#].*$", "", tok)
    return unquote(tok).strip().rstrip(".,:;!?*").strip("/").lower()


def strip_page_ext(name):
    for ext in PAGE_EXT:
        if name.endswith(ext):
            return name[: -len(ext)]
    return name


def walk(top):
    for dp, dns, fns in os.walk(top):
        dns[:] = [d for d in dns if d not in SKIP_DIRS and not d.startswith(".")]
        for fn in fns:
            yield os.path.join(dp, fn)


def main():
    ap = argparse.ArgumentParser(description="Find unused files in a contents folder.")
    ap.add_argument("contents", help="folder whose files should be checked")
    ap.add_argument(
        "--root", default=".", help="project root to search in (default: .)"
    )
    ap.add_argument(
        "--ignore",
        action="append",
        default=[],
        metavar="GLOB",
        help="glob of files to skip (repeatable)",
    )
    args = ap.parse_args()

    contents = os.path.abspath(args.contents)
    root = os.path.abspath(args.root)
    if not os.path.isdir(contents):
        sys.exit(f"Not a folder: {contents}")

    # 1. the files to check
    targets = []
    for path in walk(contents):
        rel = os.path.relpath(path, contents).replace(os.sep, "/")
        name = os.path.basename(path)
        if name == ".DS_Store" or any(
            fnmatch.fnmatch(rel, p) or fnmatch.fnmatch(name, p) for p in args.ignore
        ):
            continue
        targets.append(path)
    spaced = {
        p: os.path.basename(p).lower() for p in targets if " " in os.path.basename(p)
    }

    # 2. scan every text file; remember which files mention which names
    names = defaultdict(set)  # "photo.png" / "guide.md" -> files mentioning it
    stems = defaultdict(set)  # "guide" (from a link target) -> files mentioning it
    spaced_hits = defaultdict(set)
    seen = set()
    for top in {root, contents}:
        for path in walk(top):
            if path in seen:
                continue
            seen.add(path)
            try:
                if os.path.getsize(path) > MAX_SIZE:
                    continue
                with open(path, "rb") as f:
                    raw = f.read()
            except OSError:
                continue
            if b"\0" in raw[:4096]:
                continue  # binary file
            text = raw.decode("utf-8", errors="replace").lower()

            for tok in SPLIT.split(text):
                t = clean(tok)
                if t:
                    names[os.path.basename(t)].add(path)
            for rx in LINK_RES:
                for link in rx.findall(text):
                    t = clean(link)
                    if t:
                        stems[strip_page_ext(os.path.basename(t))].add(path)
            for tpath, lname in spaced.items():
                if lname in text or lname.replace(" ", "%20") in text:
                    spaced_hits[tpath].add(path)

    # 3. decide which targets are used
    unused = []
    for path in targets:
        name = os.path.basename(path).lower()
        refs = set(names.get(name, ())) | spaced_hits.get(path, set())
        if name.endswith(PAGE_EXT):
            stem = strip_page_ext(name)
            keys = {stem, re.sub(r"^\d{4}-\d{2}-\d{2}-", "", stem)}  # posts: drop date
            if stem in ("index", "readme"):
                keys.add(
                    os.path.basename(os.path.dirname(path)).lower()
                )  # link to folder/
            for k in keys:
                refs |= stems.get(k, set())
        refs.discard(path)
        if not refs:
            unused.append(path)

    # 4. report
    unused.sort()
    print(f"Files checked : {len(targets)}")
    print(f"Used          : {len(targets) - len(unused)}")
    print(f"Unused        : {len(unused)}")
    if unused:
        print()
        for p in unused:
            print(os.path.relpath(p, root if p.startswith(root) else contents))


if __name__ == "__main__":
    main()

##################################################################################################
# USAGE

# List files (all filetypes) in a folder that no other file refers to.
#   A file counts as "used" if its file name appears anywhere in another text file
#   A link without extension also counts
#   Matching is case-insensitive and by file name, not full path.

# Usage:
#     python3 find_unused.py <dir>
#     python3 find_unused.py content --root /path/to/project
#     python3 find_unused.py content --ignore "*.psd" --ignore "drafts/*"
