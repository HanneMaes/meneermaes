#!/usr/bin/env python3

import os
import re
import sys
import shutil
import zipfile
import tempfile
import subprocess
from pathlib import Path
from datetime import datetime
from html import escape

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
            return yaml.safe_load(f) or {}
    except Exception as e:
        print(f"{RED}✗ Error loading {settings_path}: {e}{NC}\n")
        sys.exit(1)


#############################################################################
# Helpers


def _fmt_num(number):
    """Format a number without an unnecessary .0."""
    if number is None:
        return ""

    number = float(number)

    if number.is_integer():
        return str(int(number))

    return str(round(number, 2))


def _escape_xml(value):
    return escape(str(value), quote=False)


def find_matching_input_yaml(input_dir, assignment_basename):
    """Find the original YAML file belonging to an assignment folder."""
    input_dir = Path(input_dir)

    if not input_dir.exists():
        return None

    for yaml_file in input_dir.rglob("*.yaml"):
        yaml_name = yaml_file.stem.replace("-", " ")

        if yaml_name == assignment_basename:
            return yaml_file

    return None


def resolve_vak(input_yaml, input_dir):
    """Determine the subject from the first directory below input_dir."""
    if input_yaml is None:
        return None

    try:
        relative_path = input_yaml.relative_to(input_dir)
        return relative_path.parts[0]
    except (ValueError, IndexError):
        return None


def extract_class_name(assignment_dir, output_dir):
    """
    Extract only the class from a path such as:

        output/6AD - flex/flex/taak

    or:

        output/6AD - flex/taak

    The class is always the first path component. The part before the first
    ' - ' is used as the actual class name (so 'flex' is not duplicated).
    """
    relative_parts = assignment_dir.relative_to(output_dir).parts

    if not relative_parts:
        return assignment_dir.name

    first_folder = relative_parts[0]

    if " - " in first_folder:
        return first_folder.split(" - ", 1)[0].strip()

    return first_folder


#############################################################################
# Reading ODS files


def read_ods_data(ods_path):
    """
    Read scores and totals from an ODS file.

    Returns:
        items, total_score, total_max, late, eindscore, late_penalty
    """
    document = load_ods(str(ods_path))
    tables = document.spreadsheet.getElementsByType(Table)

    if not tables:
        raise ValueError(f"No table found in {ods_path}")

    table = tables[0]
    rows = table.getElementsByType(TableRow)

    total_row_index = None

    for index, row in enumerate(rows):
        cells = row.getElementsByType(TableCell)

        if not cells:
            continue

        first_cell_text = extractText(cells[0]).strip().upper()

        if first_cell_text == "TOTAAL":
            total_row_index = index
            break

    if total_row_index is None:
        raise ValueError(f"No TOTAAL row found in {ods_path}")

    items = []

    for row in rows[1:total_row_index]:
        cells = row.getElementsByType(TableCell)

        if len(cells) < 4:
            continue

        description = extractText(cells[0]).strip()
        score_raw = cells[1].getAttribute("value")
        maximum_raw = cells[3].getAttribute("value")

        score = float(score_raw) if score_raw not in (None, "") else None
        maximum = float(maximum_raw) if maximum_raw not in (None, "") else 0.0

        items.append(
            {
                "desc": description,
                "score": score,
                "max": maximum,
            }
        )

    total_cells = rows[total_row_index].getElementsByType(TableCell)

    total_score_raw = total_cells[1].getAttribute("value")
    total_max_raw = total_cells[3].getAttribute("value")

    if total_score_raw not in (None, ""):
        total_score = float(total_score_raw)
    else:
        total_score = sum(item["score"] or 0 for item in items)

    if total_max_raw not in (None, ""):
        total_max = float(total_max_raw)
    else:
        total_max = sum(item["max"] for item in items)

    late = False
    late_penalty = 0.0
    eindscore = total_score

    te_laat_row_index = total_row_index + 1

    if te_laat_row_index < len(rows):
        te_laat_cells = rows[te_laat_row_index].getElementsByType(TableCell)

        if te_laat_cells:
            te_laat_label = extractText(te_laat_cells[0]).strip().upper()

            if te_laat_label.startswith("TE LAAT"):
                late = extractText(te_laat_cells[1]).strip() != ""

                if len(te_laat_cells) > 2:
                    penalty_raw = te_laat_cells[2].getAttribute("value")

                    if penalty_raw not in (None, ""):
                        late_penalty = float(penalty_raw)

    eindscore_row_index = total_row_index + 2

    if eindscore_row_index < len(rows):
        eindscore_cells = rows[eindscore_row_index].getElementsByType(TableCell)

        if eindscore_cells:
            eindscore_label = extractText(eindscore_cells[0]).strip().upper()

            if eindscore_label == "EINDSCORE":
                eindscore_raw = eindscore_cells[1].getAttribute("value")

                if eindscore_raw not in (None, ""):
                    eindscore = float(eindscore_raw)
                elif late:
                    eindscore = round(total_score * 0.8, 2)

    return items, total_score, total_max, late, eindscore, late_penalty


#############################################################################
# Reading Doelen


def read_doelen_marks(ods_path):
    """Read the Doelen section from the same ODS sheet, if present."""
    document = load_ods(str(ods_path))
    tables = document.spreadsheet.getElementsByType(Table)

    if not tables:
        return []

    table = tables[0]
    rows = table.getElementsByType(TableRow)

    doelen_header_index = None

    for index, row in enumerate(rows):
        cells = row.getElementsByType(TableCell)

        if not cells:
            continue

        first_cell_text = extractText(cells[0]).strip()

        if (
            first_cell_text.startswith("V: Niet bereid tot.")
            or first_cell_text == "Doelstelling"
        ):
            doelen_header_index = index
            break

    if doelen_header_index is None:
        return []

    letters = ["V", "B", "G", "E"]
    doelen = []

    for row in rows[doelen_header_index + 1 :]:
        cells = row.getElementsByType(TableCell)

        if not cells:
            continue

        label = extractText(cells[0]).strip()

        if not label:
            continue

        if len(cells) < 5:
            continue

        if " - " in label:
            number, description = label.split(" - ", 1)
        else:
            number = ""
            description = label

        marked_letters = []

        for letter, cell in zip(letters, cells[1:5]):
            value = extractText(cell).strip().lower()

            if value == "x":
                marked_letters.append(letter)

        marked = marked_letters[0] if marked_letters else None
        ambiguous = len(marked_letters) > 1

        doelen.append(
            {
                "nr": number,
                "desc": description,
                "marked": marked,
                "ambiguous": ambiguous,
            }
        )

    return doelen


#############################################################################
# Building the score table (Punten)


def build_score_table_xml(
    items,
    total_score,
    total_max,
    late,
    eindscore,
    late_penalty,
):
    """
    Build the ODF table that replaces {{SCORE}}.

    Column widths are defined via proper ODF automatic table-column styles
    (style:style family="table-column"), referenced from each
    table:table-column by table:style-name.

    Cells use plain <text:p> paragraphs. Bold/italic formatting is applied
    later to the complete generated document.
    """

    def cell(text):
        return (
            '<table:table-cell office:value-type="string">'
            f"<text:p>{_escape_xml(text)}</text:p>"
            "</table:table-cell>"
        )

    rows_xml = []

    rows_xml.append(
        "<table:table-row>"
        + cell("Punten")
        + cell("")
        + cell("")
        + cell("")
        + "</table:table-row>"
    )

    for item in items:
        score_text = "" if item["score"] is None else _fmt_num(item["score"])

        rows_xml.append(
            "<table:table-row>"
            + cell(item["desc"])
            + cell(score_text)
            + cell("/")
            + cell(_fmt_num(item["max"]))
            + "</table:table-row>"
        )

    if late:
        rows_xml.append(
            "<table:table-row>"
            + cell("TOTAAL")
            + cell(_fmt_num(total_score))
            + cell("/")
            + cell(_fmt_num(total_max))
            + "</table:table-row>"
        )

        rows_xml.append(
            "<table:table-row>"
            + cell("Te laat (-20%)")
            + cell(_fmt_num(late_penalty))
            + cell("")
            + cell("")
            + "</table:table-row>"
        )

    rows_xml.append(
        "<table:table-row>"
        + cell("EINDSCORE")
        + cell(_fmt_num(eindscore))
        + cell("/")
        + cell(_fmt_num(total_max))
        + "</table:table-row>"
    )

    column_styles_xml = (
        '<style:style style:name="ScoreColDesc" style:family="table-column">'
        "<style:table-column-properties "
        'fo:break-before="auto" '
        'style:column-width="13.8cm"/>'
        "</style:style>"
        '<style:style style:name="ScoreColScore" style:family="table-column">'
        "<style:table-column-properties "
        'fo:break-before="auto" '
        'style:column-width="0.9cm"/>'
        "</style:style>"
        '<style:style style:name="ScoreColSlash" style:family="table-column">'
        "<style:table-column-properties "
        'fo:break-before="auto" '
        'style:column-width="0.4cm"/>'
        "</style:style>"
        '<style:style style:name="ScoreColMax" style:family="table-column">'
        "<style:table-column-properties "
        'fo:break-before="auto" '
        'style:column-width="1.1cm"/>'
        "</style:style>"
    )

    table_xml = (
        '<table:table table:name="ScoreTable">'
        '<table:table-column table:style-name="ScoreColDesc"/>'
        '<table:table-column table:style-name="ScoreColScore"/>'
        '<table:table-column table:style-name="ScoreColSlash"/>'
        '<table:table-column table:style-name="ScoreColMax"/>'
        + "".join(rows_xml)
        + "</table:table>"
    )

    return column_styles_xml, table_xml


#############################################################################
# Building Doelen rows inside the template table


def build_doelen_rows_xml(doelen_marks):
    """
    Build table rows for the existing {{DOEL}} row in the template.

    The template's existing Doelen table is preserved. Only the row
    containing {{DOEL}} is replaced.
    """

    def cell(text):
        return (
            '<table:table-cell office:value-type="string">'
            f"<text:p>{_escape_xml(text)}</text:p>"
            "</table:table-cell>"
        )

    rows_xml = []

    for doel in doelen_marks:
        number = doel["nr"]
        description = doel["desc"]
        marked = doel["marked"] or ""

        if number:
            label = f"{number} - {description}"
        else:
            label = description

        rows_xml.append(
            "<table:table-row>" + cell(label) + cell(marked) + "</table:table-row>"
        )

    return "".join(rows_xml)


#############################################################################
# Template manipulation


def _placeholder_pattern(key):
    """
    Build a regex that matches {{KEY}} even when LibreOffice has split the
    placeholder across multiple <text:span> tags.

    Any XML tags between the braces and the key are tolerated.
    """
    return re.compile(
        r"\{\{\s*(?:<[^>]+>)*\s*" + re.escape(key) + r"\s*(?:<[^>]+>)*\s*\}\}"
    )


def replace_placeholder_in_xml(content, key, value):
    """Replace {{KEY}} (plain or split across spans) with value."""
    escaped_value = _escape_xml(value)
    pattern = _placeholder_pattern(key)
    return pattern.sub(escaped_value, content)


def replace_doel_table(content, doelen_marks):
    """
    Replace the table row containing {{DOEL}}.

    If doelen exist:
        {{DOEL}} row -> one row per doel.

    If there are no doelen:
        remove the complete table containing {{DOEL}}.

    The existing template table styling is preserved.
    """

    doel_pattern = _placeholder_pattern("DOEL")
    match = doel_pattern.search(content)

    if not match:
        return content

    doel_index = match.start()

    #########################################################################
    # Find the table containing {{DOEL}}

    table_start = content.rfind(
        "<table:table",
        0,
        doel_index,
    )

    table_end = content.find(
        "</table:table>",
        doel_index,
    )

    if table_start == -1 or table_end == -1:
        print(
            f"{RED}⚠ {{{{DOEL}}}} found, but surrounding table could not "
            f"be identified.{NC}",
            file=sys.stderr,
        )
        return content

    table_end += len("</table:table>")

    #########################################################################
    # No doelen -> remove complete table

    if not doelen_marks:
        return content[:table_start] + content[table_end:]

    #########################################################################
    # Find the row containing {{DOEL}}

    row_start = content.rfind(
        "<table:table-row",
        table_start,
        doel_index,
    )

    row_end_marker = "</table:table-row>"

    row_end = content.find(
        row_end_marker,
        doel_index,
    )

    if row_start == -1 or row_end == -1 or row_end > table_end:
        print(
            f"{RED}⚠ {{{{DOEL}}}} found, but its table row could not "
            f"be identified.{NC}",
            file=sys.stderr,
        )
        return content

    row_end += len(row_end_marker)

    #########################################################################
    # Replace {{DOEL}} row with one row per doel

    doel_rows = build_doelen_rows_xml(doelen_marks)

    return content[:row_start] + doel_rows + content[row_end:]


def make_all_text_bold_italic(content):
    """
    Make all text in the generated document bold and italic.

    A new automatic text style is added to the generated ODT. The original
    template file is not modified.
    """

    marker = "</office:automatic-styles>"

    style_xml = (
        "<style:style "
        'style:name="ForceBoldItalic" '
        'style:family="text">'
        "<style:text-properties "
        'fo:font-weight="bold" '
        'fo:font-style="italic"/>'
        "</style:style>"
    )

    #########################################################################
    # Add the new style

    if marker in content:
        content = content.replace(
            marker,
            style_xml + marker,
            1,
        )

    #########################################################################
    # Apply the style to every text:p that does not already have a style

    content = re.sub(
        r"<text:p(?![^>]*\btext:style-name=)([^>]*)>",
        r'<text:p\1 text:style-name="ForceBoldItalic">',
        content,
    )

    #########################################################################
    # Apply the style to every text:span that does not already have a style

    content = re.sub(
        r"<text:span(?![^>]*\btext:style-name=)([^>]*)>",
        r'<text:span\1 text:style-name="ForceBoldItalic">',
        content,
    )

    return content


def fill_template(
    template_path,
    replacements,
    score_parts,
    doelen_marks,
    out_odt_path,
):
    """
    Copy the template and replace all placeholders.

    SCORE:
        Replaced by a generated score table.

    DOEL:
        The existing template row containing {{DOEL}} is replaced with one
        row per doel. If there are no doelen, the complete table containing
        {{DOEL}} is removed.

    Finally, all document text is made bold and italic.
    """

    shutil.copy(template_path, out_odt_path)

    with zipfile.ZipFile(out_odt_path, "r") as input_zip:
        infos = input_zip.infolist()
        content = input_zip.read("content.xml").decode("utf-8")

        other_files = [
            (info, input_zip.read(info.filename))
            for info in infos
            if info.filename != "content.xml"
        ]

    #########################################################################
    # Normal placeholders

    for key, value in replacements.items():
        content = replace_placeholder_in_xml(
            content,
            key,
            value,
        )

    #########################################################################
    # SCORE

    score_column_styles, score_table_xml = score_parts

    score_pattern = re.compile(
        r"<text:p(?:\s[^>]*)?>"
        r"\s*(?:<[^>]+>)*"
        r"\{\{\s*(?:<[^>]+>)*\s*SCORE\s*(?:<[^>]+>)*\s*\}\}"
        r"\s*(?:<[^>]+>)*"
        r"</text:p>"
    )

    content, score_replacements = score_pattern.subn(
        score_table_xml,
        content,
        count=1,
    )

    if score_replacements == 0:
        print(
            f"{RED}✗ Warning: {{{{SCORE}}}} placeholder paragraph not found - "
            f"the score table was not inserted. Check the template's "
            f"content.xml for how {{{{SCORE}}}} is stored.{NC}",
            file=sys.stderr,
        )

    #########################################################################
    # DOEL

    content = replace_doel_table(
        content,
        doelen_marks,
    )

    #########################################################################
    # Register score table column styles

    if score_column_styles:
        marker = "</office:automatic-styles>"

        if marker in content:
            content = content.replace(
                marker,
                score_column_styles + marker,
                1,
            )
        else:
            print(
                f"{RED}✗ Warning: <office:automatic-styles> not found - "
                f"column widths may fall back to defaults.{NC}",
                file=sys.stderr,
            )

    #########################################################################
    # Make everything bold + italic

    content = make_all_text_bold_italic(content)

    #########################################################################
    # Write modified ODT

    with zipfile.ZipFile(out_odt_path, "w") as output_zip:
        for info, data in other_files:
            compression = (
                zipfile.ZIP_STORED
                if info.filename == "mimetype"
                else zipfile.ZIP_DEFLATED
            )

            output_zip.writestr(
                info,
                data,
                compress_type=compression,
            )

        output_zip.writestr(
            "content.xml",
            content,
            compress_type=zipfile.ZIP_DEFLATED,
        )


#############################################################################
# PDF conversion


def convert_to_pdf(odt_path, output_directory):
    """Convert an ODT file to PDF using headless LibreOffice."""
    with tempfile.TemporaryDirectory() as profile_directory:
        subprocess.run(
            [
                "soffice",
                "--headless",
                f"-env:UserInstallation=file://{profile_directory}",
                "--convert-to",
                "pdf",
                "--outdir",
                str(output_directory),
                str(odt_path),
            ],
            check=True,
            capture_output=True,
        )


def save_folder_to_open(folder_path):
    """Save folder path for opening by the host after the container exits."""
    in_docker = Path("/.dockerenv").exists()

    if in_docker:
        with open("/tmp/maesbot_output_dir/folder", "w") as output_file:
            output_file.write(str(folder_path))

        print(
            f"{DARK_GREY}Folder will open automatically after script completes{NC}",
            file=sys.stderr,
        )
    else:
        try:
            subprocess.run(
                ["xdg-open", str(folder_path)],
                check=True,
            )
        except (
            subprocess.CalledProcessError,
            FileNotFoundError,
        ):
            print(
                f"{DARK_GREY}Path: {folder_path}{NC}",
                file=sys.stderr,
            )


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

    #########################################################################
    # Check directories and template

    if not output_dir.exists():
        print(f"{RED}✗ Error: output directory does not exist: {output_dir}{NC}\n")
        sys.exit(1)

    if not output_dir_pdf.parent.exists():
        print(
            f"{RED}✗ Error: parent of PDF output directory does not exist: "
            f"{output_dir_pdf.parent}{NC}\n"
        )
        sys.exit(1)

    output_dir_pdf.mkdir(
        parents=True,
        exist_ok=True,
    )

    if not template_path.exists():
        print(f"{RED}✗ Error: template not found at {template_path}{NC}\n")
        sys.exit(1)

    #########################################################################
    # Find generated sheets

    leaf_directories = []

    for directory_path, _directory_names, filenames in os.walk(output_dir):
        if any(filename.endswith(".ods") for filename in filenames):
            leaf_directories.append(Path(directory_path))

    if not leaf_directories:
        print(f"{RED}✗ No generated sheets found under {output_dir}{NC}\n")
        sys.exit(1)

    #########################################################################
    # Select assignment

    display_to_path = {
        str(path.relative_to(output_dir)): path for path in sorted(leaf_directories)
    }

    selected_display = pick_from_list(
        list(display_to_path.keys()),
        "Select class/assignment:",
        message_color="#87d7d7",
    )

    if not selected_display:
        print(f"{YELLOW}No assignment selected{NC}\n")
        sys.exit(1)

    assignment_dir = display_to_path[selected_display]

    assignment_basename = assignment_dir.name

    klas = extract_class_name(
        assignment_dir,
        output_dir,
    )

    #########################################################################
    # Find matching YAML

    input_yaml = find_matching_input_yaml(
        input_dir,
        assignment_basename,
    )

    title = assignment_basename

    if input_yaml:
        print(
            f"{DARK_GREY}Loaded input YAML from {input_yaml}{NC}",
            file=sys.stderr,
        )

        with open(input_yaml) as input_file:
            yaml_data = yaml.safe_load(input_file) or {}

        title = yaml_data.get(
            "title",
            title,
        )

    else:
        print(
            f"{YELLOW}⚠ No matching input YAML found for "
            f"'{assignment_basename}' under {input_dir}. "
            f"Using folder name as title.{NC}",
            file=sys.stderr,
        )

    #########################################################################
    # Determine vak

    vak = resolve_vak(
        input_yaml,
        input_dir,
    )

    if not vak:
        vak = input(f"{YELLOW}Vak voor '{title}': {NC}").strip()

    #########################################################################
    # Find ODS files

    ods_files = sorted(assignment_dir.glob("*.ods"))

    if not ods_files:
        print(f"{RED}✗ No .ods files found in {assignment_dir}{NC}\n")
        sys.exit(1)

    print(
        f"{DARK_GREY}Klas: {klas} | Vak: {vak} | Titel: {title}{NC}",
        file=sys.stderr,
    )

    #########################################################################
    # Output directory

    target_directory = output_dir_pdf / f"{klas} - {vak}" / assignment_basename

    target_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    today = datetime.now().strftime("%d/%m/%Y")

    created_files = []
    moved_ods_count = 0

    #########################################################################
    # Process each student

    for ods_path in ods_files:
        student_name = ods_path.stem.split(" - ", 1)[0].strip()

        #####################################################################
        # Read scores

        try:
            (
                items,
                total_score,
                total_max,
                late,
                eindscore,
                late_penalty,
            ) = read_ods_data(ods_path)

        except Exception as error:
            print(f"{RED}✗ Skipping {ods_path.name}: {error}{NC}")
            continue

        if any(item["score"] is None for item in items):
            print(
                f"{YELLOW}⚠ {student_name}: some items are "
                f"not graded yet. Generating PDF anyway.{NC}"
            )

        #####################################################################
        # Read doelen

        doelen_marks = read_doelen_marks(ods_path)

        if any(doel["marked"] is None for doel in doelen_marks):
            print(
                f"{YELLOW}⚠ {student_name}: one or more doelen "
                f"have no V/B/G/E mark.{NC}"
            )

        if any(doel["ambiguous"] for doel in doelen_marks):
            print(
                f"{RED}⚠ {student_name}: one or more doelen "
                f"have multiple V/B/G/E marks.{NC}"
            )

        #####################################################################
        # Replacements

        replacements = {
            "NAAM": student_name,
            "DATUM": today,
            "TOTAAL": (f"{_fmt_num(eindscore)}/{_fmt_num(total_max)}"),
            "VAK": vak,
            "KLAS": klas,
            "TITEL": title,
        }

        #####################################################################
        # Build score table

        score_parts = build_score_table_xml(
            items=items,
            total_score=total_score,
            total_max=total_max,
            late=late,
            eindscore=eindscore,
            late_penalty=late_penalty,
        )

        #####################################################################
        # Create temporary ODT

        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_odt_path = Path(temporary_directory) / f"{student_name}.odt"

            fill_template(
                template_path=template_path,
                replacements=replacements,
                score_parts=score_parts,
                doelen_marks=doelen_marks,
                out_odt_path=temporary_odt_path,
            )

            #################################################################
            # Convert to PDF

            try:
                convert_to_pdf(
                    temporary_odt_path,
                    target_directory,
                )

            except subprocess.CalledProcessError as error:
                print(f"{RED}✗ Failed to convert {student_name} to PDF: {error}{NC}")
                continue

        #####################################################################
        # Rename PDF

        generated_pdf = target_directory / f"{student_name}.pdf"

        final_pdf = target_directory / f"{student_name} - {title}.pdf"

        if generated_pdf.exists():
            generated_pdf.replace(final_pdf)

            created_files.append(final_pdf)

            print(
                f"{BLUE}📄 Created: {final_pdf.name}{DARK_GREY}",
                file=sys.stderr,
            )

            #################################################################
            # Move ODS

            shutil.move(
                str(ods_path),
                str(target_directory / ods_path.name),
            )

            moved_ods_count += 1

        else:
            print(f"{RED}✗ Expected PDF not found for {student_name}{NC}")

    #########################################################################
    # Summary

    print()

    print(
        f"Successfully created "
        f"{len(created_files)} PDF(s) and moved "
        f"{moved_ods_count} sheet(s) to: "
        f"{target_directory}{NC}"
    )

    #########################################################################
    # Remove empty directories

    try:
        if not any(assignment_dir.iterdir()):
            assignment_dir.rmdir()

            class_directory = assignment_dir.parent

            if class_directory != output_dir and not any(class_directory.iterdir()):
                class_directory.rmdir()

                if output_dir.exists() and not any(output_dir.iterdir()):
                    output_dir.rmdir()

    except OSError:
        pass

    #########################################################################
    # Open output folder

    save_folder_to_open(target_directory)


if __name__ == "__main__":

