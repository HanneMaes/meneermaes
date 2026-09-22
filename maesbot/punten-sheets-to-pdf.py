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

        if not relative_path.parts:
            return None

        return relative_path.parts[0]

    except (ValueError, IndexError):
        return None


def extract_class_name(assignment_dir, output_dir):
    """
    Extract the class from a path such as:

        output/6AD - flex/flex/taak

    The first directory is treated as the class directory.
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

        items,
        total_score,
        total_max,
        late,
        eindscore,
        late_penalty
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

    #########################################################################
    # Individual points

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

    #########################################################################
    # Total

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

    #########################################################################
    # Late

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

    #########################################################################
    # Eindscore

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
                    eindscore = round(
                        total_score * 0.8,
                        2,
                    )

    return (
        items,
        total_score,
        total_max,
        late,
        eindscore,
        late_penalty,
    )


#############################################################################
# Reading Doelen


def read_doelen_marks(ods_path):
    """
    Read the Doelen section from the ODS.

    Expected columns:

        Doelstelling | V | B | G | E
    """

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

        #####################################################################
        # Split number and description

        if " - " in label:
            number, description = label.split(
                " - ",
                1,
            )

        else:
            number = ""
            description = label

        #####################################################################
        # Find selected V/B/G/E

        marked_letters = []

        for letter, cell in zip(
            letters,
            cells[1:5],
        ):
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
# Placeholder replacement
#
# IMPORTANT:
#
# The template already contains the correct formatting.
#
# Therefore we NEVER create a new formatting style for normal placeholders.
# We only replace the text inside the existing XML structure.


def _placeholder_pattern(key):
    """
    Find {{KEY}} even when LibreOffice has split the text over XML tags.
    """

    return re.compile(
        r"\{\{"
        r"\s*"
        r"(?:<[^>]+>)*"
        r"\s*" + re.escape(key) + r"\s*"
        r"(?:<[^>]+>)*"
        r"\s*"
        r"\}\}",
        re.DOTALL,
    )


def replace_placeholder_preserve_formatting(
    content,
    key,
    value,
):
    """
    Replace only the text of a placeholder.

    Existing XML formatting remains untouched.

    For example:

        <text:p text:style-name="P4">{{NAAM}}</text:p>

    becomes:

        <text:p text:style-name="P4">Hanne Maes</text:p>

    And:

        <text:p text:style-name="P3">
            <text:span text:style-name="T4">{{TOTAAL}}</text:span>
        </text:p>

    keeps both P3 and T4.
    """

    pattern = _placeholder_pattern(key)

    matches = list(pattern.finditer(content))

    if not matches:
        return content

    escaped_value = _escape_xml(value)

    #########################################################################
    # Replace backwards so positions remain valid.

    for match in reversed(matches):
        fragment = match.group(0)

        #####################################################################
        # Split XML tags from text.

        parts = re.split(
            r"(<[^>]+>)",
            fragment,
        )

        text_indexes = []

        for index, part in enumerate(parts):
            if not part:
                continue

            if part.startswith("<"):
                continue

            text_indexes.append(index)

        #####################################################################
        # Replace the first text section.

        if text_indexes:
            first_index = text_indexes[0]

            parts[first_index] = escaped_value

            #################################################################
            # Remove any additional text fragments.
            #
            # XML tags remain untouched.

            for index in text_indexes[1:]:
                parts[index] = ""

            replacement = "".join(parts)

        else:
            replacement = fragment

        #####################################################################
        # Insert replacement.

        content = content[: match.start()] + replacement + content[match.end() :]

    return content


#############################################################################
# Doelen table


def replace_selected_checkbox(
    row_xml,
    marked,
):
    """
    Replace the selected checkbox with V.

    The template has four columns:

        V | B | G | E

    We only replace the checkbox belonging to the selected value.
    """

    if not marked:
        return row_xml

    checkbox_map = {
        "V": 0,
        "B": 1,
        "G": 2,
        "E": 3,
    }

    selected_index = checkbox_map.get(marked)

    if selected_index is None:
        return row_xml

    #########################################################################
    # Find all checkbox characters.

    checkbox_matches = list(
        re.finditer(
            r"☐|&#x2610;|&#9744;",
            row_xml,
            re.IGNORECASE,
        )
    )

    if selected_index >= len(checkbox_matches):
        return row_xml

    checkbox = checkbox_matches[selected_index]

    return row_xml[: checkbox.start()] + "V" + row_xml[checkbox.end() :]


def replace_doel_table(
    content,
    doelen_marks,
):
    """
    Replace the template row containing {{DOEL}}.

    The existing row is duplicated rather than creating a new row.

    This means:

    - existing table formatting stays intact
    - existing cell styles stay intact
    - existing P4 text formatting stays intact
    - existing checkbox formatting stays intact
    """

    doel_pattern = _placeholder_pattern("DOEL")

    match = doel_pattern.search(content)

    if not match:
        print(
            f"{YELLOW}⚠ {{DOEL}} placeholder not found in template.{NC}",
            file=sys.stderr,
        )

        return content

    #########################################################################
    # Find table row containing {{DOEL}}

    row_start_matches = list(
        re.finditer(
            r"<table:table-row(?:\s[^>]*)?>",
            content[: match.start()],
            re.DOTALL,
        )
    )

    if not row_start_matches:
        print(
            f"{RED}✗ Could not find table row containing {{DOEL}}.{NC}",
            file=sys.stderr,
        )

        return content

    row_start = row_start_matches[-1].start()

    row_end = content.find(
        "</table:table-row>",
        match.end(),
    )

    if row_end == -1:
        print(
            f"{RED}✗ Could not find end of {{DOEL}} row.{NC}",
            file=sys.stderr,
        )

        return content

    row_end += len("</table:table-row>")

    row_xml = content[row_start:row_end]

    #########################################################################
    # Find surrounding table

    table_start_matches = list(
        re.finditer(
            r"<table:table(?:\s[^>]*)?>",
            content[:row_start],
            re.DOTALL,
        )
    )

    if not table_start_matches:
        print(
            f"{RED}✗ Could not find table containing {{DOEL}}.{NC}",
            file=sys.stderr,
        )

        return content

    table_start = table_start_matches[-1].start()

    table_end = content.find(
        "</table:table>",
        row_end,
    )

    if table_end == -1:
        print(
            f"{RED}✗ Could not find end of Doelen table.{NC}",
            file=sys.stderr,
        )

        return content

    table_end += len("</table:table>")

    #########################################################################
    # If there are no doelen, remove the table.

    if not doelen_marks:
        return content[:table_start] + content[table_end:]

    #########################################################################
    # Create rows by cloning the original template row.

    new_rows = []

    for doel in doelen_marks:
        number = doel["nr"]
        description = doel["desc"]
        marked = doel["marked"] or ""

        if number:
            label = f"{number} - {description}"

        else:
            label = description

        #####################################################################
        # Start from the ORIGINAL template row.

        new_row = row_xml

        #####################################################################
        # Replace {{DOEL}} without touching its P4 formatting.

        new_row = replace_placeholder_preserve_formatting(
            new_row,
            "DOEL",
            label,
        )

        #####################################################################
        # Optional {{VBE}} placeholder.

        new_row = replace_placeholder_preserve_formatting(
            new_row,
            "VBE",
            marked,
        )

        #####################################################################
        # Change only the selected checkbox.

        new_row = replace_selected_checkbox(
            new_row,
            marked,
        )

        new_rows.append(new_row)

    #########################################################################
    # Replace original row with cloned rows.

    return content[:row_start] + "".join(new_rows) + content[row_end:]


#############################################################################
# Score table
#
# IMPORTANT:
#
# No new text formatting styles are created here.
#
# The template's P4 style is explicitly reused for all normal score text.
#
# The template's P14 + T5 styles are reused for "Punten" so it looks exactly
# like the existing {{TITEL}} title.


def build_score_table_xml(
    items,
    total_score,
    total_max,
    late,
    eindscore,
    late_penalty,
):
    """
    Build the score table.

    Normal table text:
        P4

    Title:
        P14 + T5

    This deliberately reuses styles from the uploaded template.
    """

    #########################################################################
    # Normal table cell

    def cell(text):
        return (
            "<table:table-cell "
            'office:value-type="string">'
            '<text:p text:style-name="P4">'
            f"{_escape_xml(text)}"
            "</text:p>"
            "</table:table-cell>"
        )

    #########################################################################
    # Rows

    rows_xml = []

    #########################################################################
    # Individual points

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

    #########################################################################
    # Total when late

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

    #########################################################################
    # Eindscore

    rows_xml.append(
        "<table:table-row>"
        + cell("EINDSCORE")
        + cell(_fmt_num(eindscore))
        + cell("/")
        + cell(_fmt_num(total_max))
        + "</table:table-row>"
    )

    #########################################################################
    # "Punten" title
    #
    # This is deliberately copied from the template's title formatting:
    #
    #   P14 = title paragraph
    #   T5  = 16pt bold text
    #
    # The uploaded template uses exactly this combination for {{TITEL}}.

    title_xml = (
        '<text:p text:style-name="P14">'
        '<text:span text:style-name="T5">'
        "Punten"
        "</text:span>"
        "</text:p>"
    )

    #########################################################################
    # Table
    #
    # No table style.
    # No paragraph style other than P4.
    # No generated formatting.
    #
    # This means the table text remains normal template text.

    table_xml = (
        title_xml + "<table:table "
        'table:name="ScoreTable">'
        "<table:table-column/>"
        "<table:table-column/>"
        "<table:table-column/>"
        "<table:table-column/>" + "".join(rows_xml) + "</table:table>"
    )

    return table_xml


#############################################################################
# Template filling


def fill_template(
    template_path,
    replacements,
    score_table_xml,
    doelen_marks,
    out_odt_path,
):
    """
    Copy template and replace placeholders.

    Existing template formatting is preserved everywhere possible.
    """

    #########################################################################
    # Copy original template.

    shutil.copy(
        template_path,
        out_odt_path,
    )

    #########################################################################
    # Read ODT.

    with zipfile.ZipFile(
        out_odt_path,
        "r",
    ) as input_zip:
        infos = input_zip.infolist()

        content = input_zip.read("content.xml").decode("utf-8")

        other_files = [
            (
                info,
                input_zip.read(info.filename),
            )
            for info in infos
            if info.filename != "content.xml"
        ]

    #########################################################################
    # Normal placeholders
    #
    # These replacements preserve the existing paragraph/span styles.

    for key, value in replacements.items():
        content = replace_placeholder_preserve_formatting(
            content,
            key,
            value,
        )

    #########################################################################
    # SCORE
    #
    # The template contains:
    #
    #     <text:p text:style-name="Standard">{{SCORE}}</text:p>
    #
    # We replace ONLY that paragraph.
    #
    # Nothing else in the document is affected.

    score_pattern = re.compile(
        r"<text:p(?:\s[^>]*)?>"
        r"\s*"
        r"(?:<[^>]+>)*"
        r"\{\{"
        r"\s*"
        r"SCORE"
        r"\s*"
        r"\}\}"
        r"\s*"
        r"(?:<[^>]+>)*"
        r"\s*"
        r"</text:p>",
        re.DOTALL,
    )

    content, score_count = score_pattern.subn(
        score_table_xml,
        content,
        count=1,
    )

    if score_count == 0:
        print(
            f"{RED}✗ Warning: {{SCORE}} paragraph not found.{NC}",
            file=sys.stderr,
        )

    #########################################################################
    # Doelen

    content = replace_doel_table(
        content,
        doelen_marks,
    )

    #########################################################################
    # Write modified ODT.
    #
    # IMPORTANT:
    #
    # We do NOT modify styles.xml.
    #
    # We do NOT add any new automatic styles.
    #
    # We therefore keep the complete template style system untouched.

    with zipfile.ZipFile(
        out_odt_path,
        "w",
    ) as output_zip:
        #####################################################################
        # Keep mimetype uncompressed.

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

        #####################################################################
        # Write content.xml.

        output_zip.writestr(
            "content.xml",
            content,
            compress_type=zipfile.ZIP_DEFLATED,
        )


#############################################################################
# PDF conversion


def convert_to_pdf(
    odt_path,
    output_directory,
):
    """Convert ODT to PDF using headless LibreOffice."""

    with tempfile.TemporaryDirectory() as profile_directory:
        subprocess.run(
            [
                "soffice",
                "--headless",
                (f"-env:UserInstallation=file://{profile_directory}"),
                "--convert-to",
                "pdf",
                "--outdir",
                str(output_directory),
                str(odt_path),
            ],
            check=True,
            capture_output=True,
        )


#############################################################################
# Open output folder


def save_folder_to_open(folder_path):
    """
    Save folder path for opening by the host after the container exits.
    """

    in_docker = Path("/.dockerenv").exists()

    if in_docker:
        output_dir = Path("/tmp/maesbot_output_dir")

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            output_dir / "folder",
            "w",
        ) as output_file:
            output_file.write(str(folder_path))

        print(
            f"{DARK_GREY}Folder will open automatically after script completes{NC}",
            file=sys.stderr,
        )

    else:
        try:
            subprocess.run(
                [
                    "xdg-open",
                    str(folder_path),
                ],
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

    paths = settings.get(
        "paths",
        {},
    )

    #########################################################################
    # Paths

    output_dir = Path(
        paths.get(
            "punten_output_dir",
            "",
        )
    )

    output_dir_pdf = Path(
        paths.get(
            "punten_output_dir_pdf",
            "",
        )
    )

    input_dir = Path(
        paths.get(
            "punten_input_dir_website",
            "",
        )
    )

    template_path = Path(
        paths.get(
            "punten_template",
            "/data/private/Punten/Templates/Taak-toets.odt",
        )
    )

    #########################################################################
    # Check directories

    if not output_dir.exists():
        print(f"{RED}✗ Error: output directory does not exist: {output_dir}{NC}\n")

        sys.exit(1)

    if not output_dir_pdf.parent.exists():
        print(
            f"{RED}"
            f"✗ Error: parent of PDF output directory does not exist: "
            f"{output_dir_pdf.parent}"
            f"{NC}\n"
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
    # Find assignment directories

    leaf_directories = []

    for (
        directory_path,
        _directory_names,
        filenames,
    ) in os.walk(output_dir):
        if any(filename.endswith(".ods") for filename in filenames):
            leaf_directories.append(Path(directory_path))

    if not leaf_directories:
        print(f"{RED}✗ No generated sheets found under {output_dir}{NC}\n")

        sys.exit(1)

    #########################################################################
    # Assignment picker

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

    #########################################################################
    # Class

    klas = extract_class_name(
        assignment_dir,
        output_dir,
    )

    #########################################################################
    # Find YAML

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
            f"{YELLOW}"
            f"⚠ No matching input YAML found for "
            f"'{assignment_basename}' under "
            f"{input_dir}. "
            f"Using folder name as title."
            f"{NC}",
            file=sys.stderr,
        )

    #########################################################################
    # Vak

    vak = resolve_vak(
        input_yaml,
        input_dir,
    )

    if not vak:
        vak = input(f"{YELLOW}Vak voor '{title}': {NC}").strip()

    if vak:
        vak = vak.capitalize()

    #########################################################################
    # ODS files

    ods_files = sorted(assignment_dir.glob("*.ods"))

    if not ods_files:
        print(f"{RED}✗ No .ods files found in {assignment_dir}{NC}\n")

        sys.exit(1)

    print(
        f"{DARK_GREY}Klas: {klas} | Vak: {vak} | Titel: {title}{NC}",
        file=sys.stderr,
    )

    #########################################################################
    # Target directory

    target_directory = output_dir_pdf / f"{klas} - {vak}" / assignment_basename

    target_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    today = datetime.now().strftime("%d/%m/%Y")

    created_files = []
    moved_ods_count = 0

    #########################################################################
    # Process students

    for ods_path in ods_files:
        student_name = ods_path.stem.split(
            " - ",
            1,
        )[0].strip()

        #####################################################################
        # Read score data

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

        #####################################################################
        # Read doelen

        doelen_marks = read_doelen_marks(ods_path)

        if any(doel["marked"] is None for doel in doelen_marks):
            print(
                f"{YELLOW}"
                f"⚠ {student_name}: one or more doelen "
                f"have no V/B/G/E mark."
                f"{NC}"
            )

        if any(doel["ambiguous"] for doel in doelen_marks):
            print(
                f"{RED}"
                f"⚠ {student_name}: one or more doelen "
                f"have multiple V/B/G/E marks."
                f"{NC}"
            )

        #####################################################################
        # Placeholders

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

        score_table_xml = build_score_table_xml(
            items=items,
            total_score=total_score,
            total_max=total_max,
            late=late,
            eindscore=eindscore,
            late_penalty=late_penalty,
        )

        #####################################################################
        # Temporary ODT

        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_odt_path = Path(temporary_directory) / f"{student_name}.odt"

            fill_template(
                template_path=template_path,
                replacements=replacements,
                score_table_xml=score_table_xml,
                doelen_marks=doelen_marks,
                out_odt_path=temporary_odt_path,
            )

            #################################################################
            # PDF

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
                f"{BLUE}📄 Created: {final_pdf.name}{NC}",
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
        f"{target_directory}"
        f"{NC}"
    )

    #########################################################################
    # Remove empty source directories

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


#############################################################################
# Entry point


if __name__ == "__main__":
    main()
