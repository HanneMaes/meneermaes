#!/usr/bin/env python3
""" """

import fnmatch
import os
import re
import sys
from collections import defaultdict
from urllib.parse import unquote

CONTENT_DIR = "content"  # folder whose files should be checked
DATA_DIR = "_data"  # Jekyll data folder (checked via site.data.<name>)
ROOT_DIR = "."  # project root to search in
IGNORE = []  # globs of files to skip, e.g. ["*.psd", "drafts/*"]

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
# site.data.foo.bar  /  site.data["foo"]["bar"]
DATA_REF = re.compile(r"""site\.data((?:\.[\w-]+|\[\s*['"][^'"]+['"]\s*\])+)""")
DATA_PART = re.compile(r"""\.([\w-]+)|\[\s*['"]([^'"]+)['"]\s*\]""")


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
    contents = os.path.abspath(CONTENT_DIR)
    data = os.path.abspath(DATA_DIR)
    root = os.path.abspath(ROOT_DIR)
    if not os.path.isdir(contents):
        sys.exit(f"Not a folder: {contents}")

    # 1. the files to check
    targets = []
    for path in walk(contents):
        rel = os.path.relpath(path, contents).replace(os.sep, "/")
        name = os.path.basename(path)
        if name == ".DS_Store" or any(
            fnmatch.fnmatch(rel, p) or fnmatch.fnmatch(name, p) for p in IGNORE
        ):
            continue
        targets.append(path)
    spaced = {
        p: os.path.basename(p).lower() for p in targets if " " in os.path.basename(p)
    }
    data_targets = []
    if os.path.isdir(data):
        data_targets = [p for p in walk(data) if os.path.basename(p) != ".DS_Store"]

    # 2. scan every text file; remember which files mention which names
    names = defaultdict(set)  # "photo.png" / "guide.md" -> files mentioning it
    stems = defaultdict(set)  # "guide" (from a link target) -> files mentioning it
    data_refs = defaultdict(set)  # "team.members" (site.data.team.members) -> files
    word_refs = defaultdict(
        set
    )  # "members" (any whole word matching a data name) -> files
    data_stems = {
        os.path.splitext(os.path.basename(p))[0].lower() for p in data_targets
    }
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
            for m in DATA_REF.finditer(text):
                parts = [a or b for a, b in DATA_PART.findall(m.group(1))]
                data_refs[".".join(parts)].add(path)
            if not path.startswith(data + os.sep):
                for w in set(re.findall(r"[\w-]+", text)):
                    if w in data_stems:
                        word_refs[w].add(path)
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

    # 3b. data files: used if site.data.<name> (or a parent/child of it) appears,
    #     or if the name (without extension) appears as a word in any non-data file
    unused_data = []
    for path in data_targets:
        rel = os.path.relpath(path, data).replace(os.sep, "/")
        key = ".".join(os.path.splitext(rel)[0].split("/")).lower()
        refs = set(
            names.get(os.path.basename(path).lower(), ())
        )  # mentioned by file name
        refs |= word_refs.get(
            os.path.splitext(os.path.basename(path))[0].lower(), set()
        )
        for ref, files in data_refs.items():
            # site.data.team  covers  team/members.yml ; site.data.team.members.x covers team/members.yml
            if ref == key or ref.startswith(key + ".") or key.startswith(ref + "."):
                refs |= files
        refs.discard(path)
        if not refs:
            unused_data.append(path)

    # 4. report
    unused.sort()
    unused_data.sort()
    print()
    print("-" * 40)
    print(f"{CONTENT_DIR}/")
    print("-" * 40)
    print(f"Files checked : {len(targets)}")
    print(f"Used          : {len(targets) - len(unused)}")
    print(f"Unused        : {len(unused)}")
    if unused:
        print()
        for p in unused:
            print(os.path.relpath(p, root if p.startswith(root) else contents))

    if data_targets:
        print()
        print("-" * 40)
        print(f"{DATA_DIR}/")
        print("-" * 40)
        print(f"Data files checked : {len(data_targets)}")
        print(f"Used               : {len(data_targets) - len(unused_data)}")
        print(f"Unused             : {len(unused_data)}")
        if unused_data:
            print()
            for p in unused_data:
                print(os.path.relpath(p, root if p.startswith(root) else data))


if __name__ == "__main__":
    main()

##################################################################################################
# USAGE

# Looks for all filetypes that is not used on another file
# Looks in contents/ and _data/
#   A file counts as "used" if its file name appears anywhere in another text file
#   A link without extension also counts
#   Matching is case-insensitive and by file name, not full path.
#   Files in _data count as used if their name without extension appears as a word
#   in any file outside _data (e.g. site.data.<name>, include params, front matter)

# Usage:
#     python3 find_unused.py
