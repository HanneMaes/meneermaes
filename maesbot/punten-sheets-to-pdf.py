#!/usr/bin/env python3
"""
Punten: Sheets to PDF

Reads filled-in grading .ods sheets (created by punten-create-sheets.py) and
generates one PDF report card per student, based on the Taak-toets.odt
template.

Requires:
  - LibreOffice ('soffice' binary) available in the container, for the
    ODT -> PDF conversion.
  - The .ods sheets must have been opened, filled in, and SAVED in
    LibreOffice Calc, so the calculated totals are cached in the file
    (this script does not evaluate spreadsheet formulas itself).
"""

import os
import re
import sys
import shutil
import zipfile
import tempfile
import subprocess
from pathlib import Path
from datetime import datetime

import yaml
from odf.opendocument import load as load_ods
from odf.table import Table, TableRow, TableCell
from odf.teletype import extractText

from lib.fuzzypicker import pick_from_list
from lib.colors import *  # noqa: F401,F403  (color constants used below)


#############################################################################
# Settings


def load_settings(settings_path="settings.yaml"):
    settings_file = Path(settings_path)
    if not settings_file.exists():
        print(f"{RED}✗ Error: {settings_path} not found!{NC}")
        sys.exit(1)
    try:
        with open(settings_file, "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"{RED}✗ Error loading {settings_path}: {e}{NC}\n")
        sys.exit(1)


#############################################################################
# Helpers


def _fmt_num(n):
    """Format a number without a trailing .0, keep 2 decimals otherwise."""
    if n is None:
        return ""
    n = float(n)
    if n.is_integer():
        return str(int(n))
    return str(round(n, 2))


def _escape_xml(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def find_matching_input_yaml(input_dir, assignment_basename):
    """Find the original punten YAML whose (dash-stripped) filename matches
    the assignment folder name, so we can reuse its 'title'."""
    input_dir = Path(input_dir)
    if not input_dir.exists():
        return None
    for yaml_file in input_dir.rglob("*.yaml"):
        name = yaml_file.stem.replace("-", " ")
        if name == assignment_basename:
            return yaml_file
    return None


def resolve_vak(input_yaml, input_dir):
    """The subject (vak) is the top-level subfolder under
    punten_input_dir_website that the input yaml lives in, e.g.
    docs/_data/hardware/servers.yaml -> vak = 'hardware'."""
    if input_yaml is None:
        return None
    try:
        return input_yaml.relative_to(input_dir).parts[0]
    except ValueError:
        return None


#############################################################################
# Reading the filled-in .ods sheet


def read_ods_data(ods_path):
    """Read graded items + totals from a sheet created by
    punten-create-sheets.py. Returns (items, total_score, total_max)."""
    doc = load_ods(str(ods_path))
    tables = doc.spreadsheet.getElementsByType(Table)
    if not tables:
        raise ValueError(f"No table found in {ods_path}")
    table = tables[0]
    rows = table.getElementsByType(TableRow)

    # rows[0] = title row, rows[1:-1] = assignment items, rows[-1] = TOTAAL
    items = []
    for row in rows[1:-1]:
        cells = row.getElementsByType(TableCell)
        desc = extractText(cells[0]).strip()
        score_raw = cells[1].getAttribute("value")
        max_raw = cells[3].getAttribute("value")
        score = float(score_raw) if score_raw not in (None, "") else None
        max_pts = float(max_raw) if max_raw not in (None, "") else 0.0
        items.append({"desc": desc, "score": score, "max": max_pts})

    total_cells = rows[-1].getElementsByType(TableCell)
    total_score_raw = total_cells[1].getAttribute("value")
    total_max_raw = total_cells[3].getAttribute("value")

    if total_score_raw not in (None, ""):
        total_score = float(total_score_raw)
    else:
        # Fallback if the file was never opened/saved in LibreOffice
        total_score = sum(i["score"] or 0 for i in items)

    if total_max_raw not in (None, ""):
        total_max = float(total_max_raw)
    else:
        total_max = sum(i["max"] for i in items)

    return items, total_score, total_max


#############################################################################
# Reading the "Doelen" tab (if present)


def read_doelen_marks(ods_path):
    """Read the Doelen tab of a graded .ods sheet, if present.

    Returns a list of dicts: {"nr", "desc", "marked", "ambiguous"} - one per
    doel row. "marked" is whichever of V/B/G/E contains an "x" (case
    insensitive), or None if none do. "ambiguous" is True if more than one
    column was marked "x" for that row (in which case the first one found,
    in V/B/G/E order, is used, but the caller should warn about it)."""
    doc = load_ods(str(ods_path))
    tables = doc.spreadsheet.getElementsByType(Table)
    doelen_tables = [t for t in tables if t.getAttribute("name") == "Doelen"]
    if not doelen_tables:
        return []

    rows = doelen_tables[0].getElementsByType(TableRow)
    # rows[0] = legend row, rows[1] = header row (Doelstelling|V|B|G|E),
    # rows[2:] = one row per doel
    letters = ["V", "B", "G", "E"]
    marks = []
    for row in rows[2:]:
        cells = row.getElementsByType(TableCell)
        if not cells:
            continue
        label = extractText(cells[0]).strip()
        if not label:
            continue

        # The sheet stores "nr - desc" combined in one cell; split it back
        # apart for the PDF (nr's are short codes with no " - " in them).
        if " - " in label:
            nr, desc = label.split(" - ", 1)
        else:
            nr, desc = "", label

        # Only an actual "x" counts as a mark - ignores stray whitespace or
        # accidental keystrokes left behind in an otherwise-empty cell.
        matched_letters = [
            letter
            for letter, cell in zip(letters, cells[1:5])
            if extractText(cell).strip().lower() == "x"
        ]
        marked = matched_letters[0] if matched_letters else None
        ambiguous = len(matched_letters) > 1

        marks.append({"nr": nr, "desc": desc, "marked": marked, "ambiguous": ambiguous})
    return marks


#############################################################################
# Building the {{SCORE}} replacement


def build_score_table_xml(items, total_score, total_max):
    """Build a raw ODF table:table XML fragment listing each graded item's
    score plus a totals row, to replace the {{SCORE}} placeholder."""

    def cell(text):
        return (
            '<table:table-cell office:value-type="string">'
            f"<text:p>{_escape_xml(text)}</text:p>"
            "</table:table-cell>"
        )

    rows_xml = [
        "<table:table-row>"
        + cell("Onderdeel")
        + cell("Score")
        + cell("Max")
        + "</table:table-row>"
    ]

    for item in items:
        score_display = "" if item["score"] is None else _fmt_num(item["score"])
        rows_xml.append(
            "<table:table-row>"
            + cell(item["desc"])
            + cell(score_display)
            + cell(_fmt_num(item["max"]))
            + "</table:table-row>"
        )

    rows_xml.append(
        "<table:table-row>"
        + cell("TOTAAL")
        + cell(_fmt_num(total_score))
        + cell(_fmt_num(total_max))
        + "</table:table-row>"
    )

    return (
        '<table:table table:name="ScoreTable">'
        "<table:table-column/><table:table-column/><table:table-column/>"
        + "".join(rows_xml)
        + "</table:table>"
    )


CHECKED_BOX = "\u2612"  # ☒ - used in the Writer template (Calc uses plain "x" instead)
UNCHECKED_BOX = "\u2610"  # ☐


def build_doelen_rows_xml(doelen_marks):
    """Build one <table:table-row> per doel for the template's 'Transversale
    eindterm' table (Table5), replacing the {{DOEL}} row with the doel's
    nr/desc (on separate lines) and marking the correct V/B/G/E box."""

    # (cell style, label text, line-break comes before the label span)
    scale_cells = [
        ("Table5.B2", "Niet bereid tot.", False),
        ("Table5.C2", "Toont soms bereidheid tot.", False),
        ("Table5.D2", "Meestal bereid tot.", True),
        ("Table5.E2", "Altijd bereid tot.", True),
    ]
    letters = ["V", "B", "G", "E"]

    rows = []
    for doel in doelen_marks:
        nr = doel["nr"]
        desc = doel["desc"]
        marked = doel["marked"]

        if nr:
            label_xml = f"{_escape_xml(nr)}<text:line-break/>{_escape_xml(desc)}"
        else:
            label_xml = _escape_xml(desc)

        cells_xml = [
            '<table:table-cell table:style-name="Table5.A2" office:value-type="string">'
            f'<text:p text:style-name="P4">{label_xml}</text:p>'
            "</table:table-cell>"
        ]
        for letter, (style, text, lb_before) in zip(letters, scale_cells):
            box = CHECKED_BOX if letter == marked else UNCHECKED_BOX
            if lb_before:
                inner = (
                    f'<text:span text:style-name="T4">{box}</text:span>'
                    "<text:line-break/>"
                    f'<text:span text:style-name="T2">{text}</text:span>'
                )
            else:
                inner = (
                    f'<text:span text:style-name="T4">{box}</text:span>'
                    f'<text:span text:style-name="T2"> <text:line-break/>{text}</text:span>'
                )
            cells_xml.append(
                f'<table:table-cell table:style-name="{style}" office:value-type="string">'
                f'<text:p text:style-name="P4">{inner}</text:p>'
                "</table:table-cell>"
            )
        rows.append(
            '<table:table-row table:style-name="Table5.1">'
            + "".join(cells_xml)
            + "</table:table-row>"
        )

    return "".join(rows)


#############################################################################
# Filling the template + converting to PDF


def fill_template(
    template_path, replacements, score_table_xml, doelen_marks, out_odt_path
):
    """Copy the template, replace {{PLACEHOLDER}} text, the {{SCORE}}
    paragraph, and the 'Transversale eindterm' (Table5) row(s), then save
    as out_odt_path."""
    shutil.copy(template_path, out_odt_path)

    with zipfile.ZipFile(out_odt_path, "r") as zin:
        infos = zin.infolist()
        content = zin.read("content.xml").decode("utf-8")
        other_files = [
            (info, zin.read(info.filename))
            for info in infos
            if info.filename != "content.xml"
        ]

    for key, value in replacements.items():
        content = content.replace(f"{{{{{key}}}}}", _escape_xml(value))

    content = re.sub(
        r"<text:p[^>]*>\{\{SCORE\}\}</text:p>",
        score_table_xml,
        content,
    )

    doel_idx = content.find("{{DOEL}}")
    if doel_idx != -1:
        row_start = content.rfind("<table:table-row", 0, doel_idx)
        row_end = content.find("</table:table-row>", doel_idx) + len(
            "</table:table-row>"
        )
        if doelen_marks:
            content = (
                content[:row_start]
                + build_doelen_rows_xml(doelen_marks)
                + content[row_end:]
            )
        else:
            # No doelen for this assignment - drop the whole Table5 table
            table_start = content.rfind("<table:table ", 0, row_start)
            table_end = content.find("</table:table>", row_end) + len("</table:table>")
            content = content[:table_start] + content[table_end:]

    with zipfile.ZipFile(out_odt_path, "w") as zout:
        for info, data in other_files:
            compress = (
                zipfile.ZIP_STORED
                if info.filename == "mimetype"
                else zipfile.ZIP_DEFLATED
            )
            zout.writestr(info, data, compress_type=compress)
        zout.writestr("content.xml", content, compress_type=zipfile.ZIP_DEFLATED)


def convert_to_pdf(odt_path, out_dir):
    """Convert an .odt file to .pdf using headless LibreOffice."""
    with tempfile.TemporaryDirectory() as profile_dir:
        subprocess.run(
            [
                "soffice",
                "--headless",
                f"-env:UserInstallation=file://{profile_dir}",
                "--convert-to",
                "pdf",
                "--outdir",
                str(out_dir),
                str(odt_path),
            ],
            check=True,
            capture_output=True,
        )


def save_folder_to_open(folder_path):
    """Save folder path to be opened by host after container exits
    (same mechanism as punten-create-sheets.py)."""
    in_docker = Path("/.dockerenv").exists()

    if in_docker:
        with open("/tmp/maesbot_output_dir/folder", "w") as f:
            f.write(str(folder_path))
        print(
            f"{DARK_GREY}Folder will open automatically after script completes{NC}",
            file=sys.stderr,
        )
    else:
        try:
            subprocess.run(["xdg-open", str(folder_path)], check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"{DARK_GREY}Path: {folder_path}{NC}", file=sys.stderr)


#############################################################################
# Main


def main():
    settings = load_settings()
    paths = settings.get("paths", {})

    output_dir = Path(paths.get("punten_output_dir", ""))
    output_dir_pdf = Path(paths.get("punten_output_dir_pdf", ""))
    input_dir = Path(paths.get("punten_input_dir_website", ""))
    template_path = Path(
        paths.get(
            "punten_template",
            "/data/private/Punten/Templates/Taak-toets.odt",
        )
    )

    if not output_dir.exists():
        print(f"{RED}✗ Error: output directory does not exist: {output_dir}{NC}\n")
        sys.exit(1)

    if not output_dir_pdf.parent.exists():
        print(
            f"{RED}✗ Error: 'paths.punten_output_dir_pdf' parent does not exist: "
            f"{output_dir_pdf.parent}{NC}\n"
        )
        sys.exit(1)
    output_dir_pdf.mkdir(parents=True, exist_ok=True)

    if not template_path.exists():
        print(
            f"{RED}✗ Error: template not found at {template_path}{NC}\n"
            f"{RED}   Add 'paths.punten_template' to settings.yaml if it lives elsewhere.{NC}\n"
        )
        sys.exit(1)

    # Find every leaf folder (klas/assignment) that actually contains sheets
    leaf_dirs = []
    for dirpath, _dirnames, filenames in os.walk(output_dir):
        if any(f.endswith(".ods") for f in filenames):
            leaf_dirs.append(Path(dirpath))

    if not leaf_dirs:
        print(f"{RED}✗ No generated sheets found under {output_dir}{NC}\n")
        sys.exit(1)

    display_to_path = {str(p.relative_to(output_dir)): p for p in sorted(leaf_dirs)}
    selected_display = pick_from_list(
        list(display_to_path.keys()),
        "Select class/assignment:",
        message_color="#87d7d7",
    )
    if not selected_display:
        print(f"{YELLOW}No assignment selected{NC}\n")
        sys.exit(1)

    assignment_dir = display_to_path[selected_display]
    klas = assignment_dir.relative_to(output_dir).parts[0]
    assignment_basename = assignment_dir.name

    # Pull the title from the matching input yaml, and derive the subject
    # (vak) from the top-level folder that yaml lives in
    input_yaml = find_matching_input_yaml(input_dir, assignment_basename)
    title = assignment_basename
    if input_yaml:
        print(f"{DARK_GREY}Loaded input YAML from {input_yaml}{NC}", file=sys.stderr)
        with open(input_yaml) as f:
            ydata = yaml.safe_load(f) or {}
        title = ydata.get("title", title)
    else:
        print(
            f"{YELLOW}⚠ No matching input YAML found for '{assignment_basename}' "
            f"under {input_dir} — falling back to folder name as title{NC}",
            file=sys.stderr,
        )

    vak = resolve_vak(input_yaml, input_dir)
    if not vak:
        vak = input(
            f"{YELLOW}Couldn't determine vak automatically. "
            f"Vak (subject) for '{title}': {NC}"
        ).strip()

    ods_files = sorted(assignment_dir.glob("*.ods"))
    if not ods_files:
        print(f"{RED}✗ No .ods files found in {assignment_dir}{NC}\n")
        sys.exit(1)

    print(f"{DARK_GREY}Klas: {klas} | Vak: {vak} | Titel: {title}{NC}", file=sys.stderr)
    print(
        f"{DARK_GREY}Generating PDFs for {len(ods_files)} student(s): "
        f"{', '.join(p.stem.split(' - ')[0] for p in ods_files)}{NC}"
    )
    print()

    # Destination folder: ".../Verbeterde taken en toetsen/{klas} - {vak}/{assignment}/"
    # (mirrors punten-create-sheets.py's output_dir/basename/ structure)
    target_dir = output_dir_pdf / f"{klas} - {vak}" / assignment_basename
    target_dir.mkdir(parents=True, exist_ok=True)

    today = datetime.now().strftime("%d/%m/%Y")
    created_files = []
    moved_ods_count = 0

    for ods_path in ods_files:
        student_name = ods_path.stem.split(" - ")[0]

        try:
            items, total_score, total_max = read_ods_data(ods_path)
        except Exception as e:
            print(f"{RED}✗ Skipping {ods_path.name}: {e}{NC}")
            continue

        if any(i["score"] is None for i in items):
            print(
                f"{YELLOW}⚠ {student_name}: some items are not graded yet, "
                f"generating PDF anyway{NC}"
            )

        doelen_marks = read_doelen_marks(ods_path)
        if any(d["marked"] is None for d in doelen_marks):
            print(
                f"{YELLOW}⚠ {student_name}: one or more doelen have no V/B/G/E "
                f"mark, leaving those boxes unchecked{NC}"
            )
        if any(d["ambiguous"] for d in doelen_marks):
            print(
                f"{RED}⚠ {student_name}: one or more doelen have MULTIPLE "
                f"V/B/G/E marks - using the first one found, please fix the "
                f"sheet and re-run{NC}"
            )

        replacements = {
            "NAAM": student_name,
            "DATUM": today,
            "TOTAAL": _fmt_num(total_score),
            "VAK": vak,
            "KLAS": klas,
            "TITEL": title,
        }
        score_table_xml = build_score_table_xml(items, total_score, total_max)

        with tempfile.TemporaryDirectory() as tmp:
            tmp_odt = Path(tmp) / f"{student_name}.odt"
            fill_template(
                template_path, replacements, score_table_xml, doelen_marks, tmp_odt
            )
            try:
                convert_to_pdf(tmp_odt, target_dir)
            except subprocess.CalledProcessError as e:
                print(f"{RED}✗ Failed to convert {student_name} to PDF: {e}{NC}")
                continue

        generated_pdf = target_dir / f"{student_name}.pdf"
        final_pdf = target_dir / f"{student_name} - {title}.pdf"
        if generated_pdf.exists():
            generated_pdf.replace(final_pdf)
            created_files.append(final_pdf)
            print(f"{BLUE}📄 Created: {final_pdf.name}{DARK_GREY}", file=sys.stderr)

            # Move the graded sheet alongside its PDF so it no longer shows
            # up as a pending assignment in punten_output_dir
            shutil.move(str(ods_path), str(target_dir / ods_path.name))
            moved_ods_count += 1
        else:
            print(f"{RED}✗ Expected PDF not found for {student_name}{NC}")

    print()
    print(
        f"Successfully created {len(created_files)} PDF(s) and moved "
        f"{moved_ods_count} sheet(s) to: {target_dir}{NC}"
    )

    # Clean up the now-empty (or partially-emptied) TO-DO folders, all the
    # way up to punten_output_dir itself if nothing is left in it
    try:
        if not any(assignment_dir.iterdir()):
            assignment_dir.rmdir()
            klas_dir = assignment_dir.parent
            if klas_dir != output_dir and not any(klas_dir.iterdir()):
                klas_dir.rmdir()
                if output_dir.exists() and not any(output_dir.iterdir()):
                    output_dir.rmdir()
                    print(
                        f"{DARK_GREY}No pending sheets left - removed {output_dir}{NC}",
                        file=sys.stderr,
                    )
    except OSError:
        pass  # leftover files (e.g. a failed conversion) - leave it as is

    save_folder_to_open(target_dir)


if __name__ == "__main__":
    main()

######################################################################################################
# GUIDE
#
# settings.yaml paths section (yours, for reference):
#   paths:
#     private_settings: "/data/private/private-settings.yaml"
#     punten_input_dir_website: "/data/input/"
#     punten_output_dir: "/data/private/Punten/Taken en toetsen - TO-DO/"
#     punten_output_dir_pdf: "/data/private/Punten/Taken en toetsen - Verbeterd/"
#     punten_template: "/data/private/Punten/Templates/Taak-toets.odt"
#
# Add to main.py:
#   actions = ["Punten: Create Sheets", "Punten: Sheets to PDF"]
#   ...
#   elif selected == "Punten: Sheets to PDF":
#       run_script("punten-sheets-to-pdf.py")
#
# (The old commented-out call used the path "Punten/sheets-to-pdf.py", which
# doesn't match the actual filename "punten-sheets-to-pdf.py" in your repo root.)
