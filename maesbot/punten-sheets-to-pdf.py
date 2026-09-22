#!/usr/bin/env python3
"""
Punten: Sheets to PDF

Reads filled-in grading .ods sheets (created by punten-create-sheets.py) and
generates one PDF report card per student, based on the Taak-toets.odt
template.

Requires:
  - LibreOffice ('soffice' binary) available in the container
  - The .ods sheets must have been opened, filled in, and SAVED in
    LibreOffice Calc
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
from lib.colors import *


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
    the assignment folder name."""
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
    punten_input_dir_website that the input yaml lives in."""
    if input_yaml is None:
        return None
    try:
        return input_yaml.relative_to(input_dir).parts[0]
    except ValueError:
        return None


#############################################################################
# Reading the filled-in .ods sheet


def read_ods_data(ods_path):
    """Read graded items + totals from a sheet.
    Returns (items, total_score, total_max, late, eindscore, late_penalty)."""
    doc = load_ods(str(ods_path))
    tables = doc.spreadsheet.getElementsByType(Table)
    if not tables:
        raise ValueError(f"No table found in {ods_path}")
    table = tables[0]
    rows = table.getElementsByType(TableRow)

    total_row_idx = None
    for i, row in enumerate(rows):
        cells = row.getElementsByType(TableCell)
        if cells and extractText(cells[0]).strip().upper() == "TOTAAL":
            total_row_idx = i
            break
    if total_row_idx is None:
        raise ValueError(f"No TOTAAL row found in {ods_path}")

    items = []
    for row in rows[1:total_row_idx]:
        cells = row.getElementsByType(TableCell)
        desc = extractText(cells[0]).strip()
        score_raw = cells[1].getAttribute("value")
        max_raw = cells[3].getAttribute("value")
        score = float(score_raw) if score_raw not in (None, "") else None
        max_pts = float(max_raw) if max_raw not in (None, "") else 0.0
        items.append({"desc": desc, "score": score, "max": max_pts})

    total_cells = rows[total_row_idx].getElementsByType(TableCell)
    total_score_raw = total_cells[1].getAttribute("value")
    total_max_raw = total_cells[3].getAttribute("value")

    if total_score_raw not in (None, ""):
        total_score = float(total_score_raw)
    else:
        total_score = sum(i["score"] or 0 for i in items)

    if total_max_raw not in (None, ""):
        total_max = float(total_max_raw)
    else:
        total_max = sum(i["max"] for i in items)

    late = False
    late_penalty = 0.0
    eindscore = total_score
    if total_row_idx + 1 < len(rows):
        te_laat_cells = rows[total_row_idx + 1].getElementsByType(TableCell)
        if te_laat_cells and extractText(te_laat_cells[0]).strip().upper().startswith(
            "TE LAAT"
        ):
            late = extractText(te_laat_cells[1]).strip() != ""
            late_penalty_raw = te_laat_cells[2].getAttribute("value")
            if late_penalty_raw not in (None, ""):
                late_penalty = float(late_penalty_raw)
    if total_row_idx + 2 < len(rows):
        eind_cells = rows[total_row_idx + 2].getElementsByType(TableCell)
        if eind_cells and extractText(eind_cells[0]).strip().upper() == "EINDSCORE":
            eind_raw = eind_cells[1].getAttribute("value")
            if eind_raw not in (None, ""):
                eindscore = float(eind_raw)
            elif late:
                eindscore = round(total_score - total_score * 0.2, 2)

    return items, total_score, total_max, late, eindscore, late_penalty


#############################################################################
# Reading the "Doelen" tab


def read_doelen_marks(ods_path):
    """Read the Doelen section of a graded .ods sheet, if present."""
    doc = load_ods(str(ods_path))
    tables = doc.spreadsheet.getElementsByType(Table)
    if not tables:
        return []
    rows = tables[0].getElementsByType(TableRow)

    header_idx = None
    for i, row in enumerate(rows):
        cells = row.getElementsByType(TableCell)
        if cells and extractText(cells[0]).strip() == "Doelstelling":
            header_idx = i
            break
    if header_idx is None:
        return []

    letters = ["V", "B", "G", "E"]
    marks = []
    for row in rows[header_idx + 1 :]:
        cells = row.getElementsByType(TableCell)
        if not cells:
            continue
        label = extractText(cells[0]).strip()
        if not label:
            continue

        if " - " in label:
            nr, desc = label.split(" - ", 1)
        else:
            nr, desc = "", label

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


def build_score_table_xml(
    items, total_score, total_max, late, eindscore, late_penalty, doelen_marks
):
    """Build a raw ODF table XML fragment listing each graded item's
    score plus a totals row, to replace the {{SCORE}} placeholder.

    Uses a plain, non-bold/non-italic paragraph style ("Standard") for every
    cell so the table inherits normal text formatting instead of picking up
    bold/italic from the surrounding template paragraph.
    """

    def cell(text, style_name="TableContentsCell"):
        return (
            f'<table:table-cell table:style-name="{style_name}" office:value-type="string">'
            f'<text:p text:style-name="Standard">{_escape_xml(text)}</text:p>'
            "</table:table-cell>"
        )

    rows_xml = []

    for item in items:
        score_display = "" if item["score"] is None else _fmt_num(item["score"])

        rows_xml.append(
            "<table:table-row>"
            + cell(item["desc"], "ScoreDescCell")
            + cell(score_display, "ScoreValCell")
            + cell("/", "ScoreSepCell")
            + cell(_fmt_num(item["max"]), "ScoreMaxCell")
            + "</table:table-row>"
        )

    if late:
        # Show TOTAAL (pre-penalty) only when relevant, followed by the
        # late penalty and the final EINDSCORE.
        rows_xml.append(
            "<table:table-row>"
            + cell("TOTAAL", "ScoreDescCell")
            + cell(_fmt_num(total_score), "ScoreValCell")
            + cell("/", "ScoreSepCell")
            + cell(_fmt_num(total_max), "ScoreMaxCell")
            + "</table:table-row>"
        )
        rows_xml.append(
            "<table:table-row>"
            + cell("Te laat (-20%)", "ScoreDescCell")
            + cell(_fmt_num(late_penalty), "ScoreValCell")
            + cell("", "ScoreSepCell")
            + cell("", "ScoreMaxCell")
            + "</table:table-row>"
        )
        rows_xml.append(
            "<table:table-row>"
            + cell("EINDSCORE", "ScoreDescCell")
            + cell(_fmt_num(eindscore), "ScoreValCell")
            + cell("/", "ScoreSepCell")
            + cell(_fmt_num(total_max), "ScoreMaxCell")
            + "</table:table-row>"
        )
    else:
        # Not late: TOTAAL and EINDSCORE are identical, so just show one
        # row, labelled EINDSCORE.
        rows_xml.append(
            "<table:table-row>"
            + cell("EINDSCORE", "ScoreDescCell")
            + cell(_fmt_num(eindscore), "ScoreValCell")
            + cell("/", "ScoreSepCell")
            + cell(_fmt_num(total_max), "ScoreMaxCell")
            + "</table:table-row>"
        )

    if doelen_marks:
        rows_xml.append(
            "<table:table-row>"
            + cell("", "ScoreDescCell")
            + cell("", "ScoreValCell")
            + cell("", "ScoreSepCell")
            + cell("", "ScoreMaxCell")
            + "</table:table-row>"
        )

        for doel in doelen_marks:
            nr = doel["nr"]
            desc = doel["desc"]
            marked = doel["marked"]

            label = f"{nr} - {desc}" if nr else desc
            mark_display = marked if marked else ""

            rows_xml.append(
                "<table:table-row>"
                + cell(f"Doel: {label}", "ScoreDescCell")
                + cell(mark_display, "ScoreValCell")
                + cell("", "ScoreSepCell")
                + cell("", "ScoreMaxCell")
                + "</table:table-row>"
            )

    return (
        '<table:table table:name="ScoreTable">'
        '<table:table-column table:style-name="ScoreDescriptionColumn"/>'
        '<table:table-column table:style-name="ScoreValueColumn"/>'
        '<table:table-column table:style-name="ScoreSeparatorColumn"/>'
        '<table:table-column table:style-name="ScoreMaxColumn"/>'
        + "".join(rows_xml)
        + "</table:table>"
    )


CHECKED_BOX = "\u2612"
UNCHECKED_BOX = "\u2610"


def build_doelen_rows_xml(doelen_marks):
    """Build one <table:table-row> per doel for the template's table."""

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
    """Copy the template, replace placeholders, and save as out_odt_path."""
    shutil.copy(template_path, out_odt_path)

    with zipfile.ZipFile(out_odt_path, "r") as zin:
        infos = zin.infolist()
        content = zin.read("content.xml").decode("utf-8")
        other_files = [
            (info, zin.read(info.filename))
            for info in infos
            if info.filename != "content.xml"
        ]

    # Plain-text replacements (NAAM, DATUM, VAK, KLAS, TITEL, TOTAAL) keep
    # whatever bold/italic formatting the {{PLACEHOLDER}} span already had
    # in the template - we only swap the text, nothing else.
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
    """Save folder path to be opened by host after container exits."""
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

    klas_vak_parts = assignment_dir.relative_to(output_dir).parts[0].split(" - ")
    klas = (
        klas_vak_parts[0]
        if klas_vak_parts
        else assignment_dir.relative_to(output_dir).parts[0]
    )

    assignment_basename = assignment_dir.name

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

    target_dir = output_dir_pdf / f"{klas} - {vak}" / assignment_basename
    target_dir.mkdir(parents=True, exist_ok=True)

    today = datetime.now().strftime("%d/%m/%Y")
    created_files = []
    moved_ods_count = 0

    for ods_path in ods_files:
        student_name = ods_path.stem.split(" - ")[0]

        try:
            items, total_score, total_max, late, eindscore, late_penalty = (
                read_ods_data(ods_path)
            )
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

        # {{NAAM}} is replaced with the actual student name derived from
        # the .ods filename (everything before " - ").
        replacements = {
            "NAAM": student_name,
            "DATUM": today,
            "TOTAAL": f"{_fmt_num(eindscore)}/{_fmt_num(total_max)}",
            "VAK": vak,
            "KLAS": klas,
            "TITEL": title,
        }
        score_table_xml = build_score_table_xml(
            items, total_score, total_max, late, eindscore, late_penalty, doelen_marks
        )

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

            shutil.move(str(ods_path), str(target_dir / ods_path.name))
            moved_ods_count += 1
        else:
            print(f"{RED}✗ Expected PDF not found for {student_name}{NC}")

    print()
    print(
        f"Successfully created {len(created_files)} PDF(s) and moved "
        f"{moved_ods_count} sheet(s) to: {target_dir}{NC}"
    )

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
        pass

    save_folder_to_open(target_dir)


if __name__ == "__main__":
    main()
