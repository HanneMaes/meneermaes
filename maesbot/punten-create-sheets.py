import os
import sys
import yaml
import argparse
import subprocess
from odf.opendocument import OpenDocumentSpreadsheet
from odf.style import (
    Style,
    TableColumnProperties,
    TableCellProperties,
    ParagraphProperties,
)
from odf.table import (
    Table,
    TableColumn,
    TableRow,
    TableCell,
)
from odf.text import P
from lib.colors import *
from pathlib import Path

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True, help="Path to input YAML file")
parser.add_argument("--output", required=True, help="Path to output directory")
parser.add_argument(
    "--class",
    dest="class_name",
    required=True,
    help="Class name",
)
parser.add_argument(
    "--students",
    nargs="+",
    required=True,
    help="List of student names (space-separated)",
)
args = parser.parse_args()

# Load YAML punten file
with open(args.input) as f:
    data = yaml.safe_load(f)

print(f"{DARK_GREY}Loaded input YAML from {args.input}{NC}", file=sys.stderr)
print(
    f"{DARK_GREY}Creating sheets for {len(args.students)} students: {', '.join(args.students)}{NC}"
)
print()

# Load settings to determine input directory
with open("settings.yaml") as f:
    settings = yaml.safe_load(f) or {}

input_dir_setting = Path(
    settings.get("paths", {}).get(
        "punten_input_dir_website",
        "/data/input",
    )
)

# Extract assignment name from the YAML filename
basename = os.path.splitext(os.path.basename(args.input))[0].replace("-", " ")

# Determine the subject (vak) from the input directory structure
input_path = Path(args.input)

try:
    vak = input_path.relative_to(input_dir_setting).parts[0]
except (ValueError, IndexError):
    vak = input_path.parent.name

# Create: output/klas - vak/opdracht/
class_vak = f"{args.class_name} - {vak}"
output_folder = os.path.join(args.output, class_vak, basename)

os.makedirs(output_folder, exist_ok=True)

# Extract data from YAML with defaults
title = data.get("title", "punten")
punten = data.get("punten", [])
doelen = data.get("doelen", [])

# Legend for the V/B/G/E evaluation scale used on the Doelen sheet
DOELEN_SCALE = [
    ("V", "Niet bereid tot."),
    ("B", "Toont soms bereidheid tot."),
    ("G", "Meestal bereid tot."),
    ("E", "Altijd bereid tot."),
]
DOELEN_DEFAULT = "G"
CHECKED = "x"
UNCHECKED = ""
DOELEN_ACCENT_COLOR = "#CD7B60"


def create_spreadsheet(student_name, assignment_name):
    """
    Create a grading spreadsheet for a specific student.

    Args:
        student_name: Name of the student
        assignment_name: Name of the assignment (from YAML filename)

    Returns:
        Path to created .ods file
    """
    doc = OpenDocumentSpreadsheet()
    table = Table(name="Grading")

    # Define column widths: Description (wide), Score, "/", Max, (unused), (unused)
    for i, width in enumerate(("15cm", "0.6cm", "0.6cm", "0.6cm", "0.6cm", "5cm")):
        style_name = f"col_{i}_{width.replace('.', '_').replace('cm', 'cm')}"
        col_style = Style(name=style_name, family="table-column")
        col_style.addElement(TableColumnProperties(columnwidth=width))
        doc.automaticstyles.addElement(col_style)
        table.addElement(TableColumn(stylename=style_name))

    # Cell styles
    grey_bg_style_name = "GreyBackground"
    grey_bg_style = Style(name=grey_bg_style_name, family="table-cell")
    grey_bg_style.addElement(TableCellProperties(backgroundcolor="#e5e5e5"))
    doc.styles.addElement(grey_bg_style)

    doelen_bg_style_name = "DoelenBackground"
    doelen_bg_style = Style(name=doelen_bg_style_name, family="table-cell")
    doelen_bg_style.addElement(TableCellProperties(backgroundcolor=DOELEN_ACCENT_COLOR))
    doc.styles.addElement(doelen_bg_style)

    green_bg_style_name = "GreenBackground"
    green_bg_style = Style(name=green_bg_style_name, family="table-cell")
    green_bg_style.addElement(TableCellProperties(backgroundcolor="#dde8cb"))
    doc.styles.addElement(green_bg_style)

    center_align_style_name = "CenterAlign"
    center_align_style = Style(name=center_align_style_name, family="table-cell")
    center_align_style.addElement(TableCellProperties())
    center_align_style.addElement(ParagraphProperties(textalign="center"))
    doc.styles.addElement(center_align_style)

    left_align_style_name = "LeftAlign"
    left_align_style = Style(name=left_align_style_name, family="table-cell")
    left_align_style.addElement(TableCellProperties())
    left_align_style.addElement(ParagraphProperties(textalign="left"))
    doc.styles.addElement(left_align_style)

    green_left_align_style_name = "GreenLeftAlign"
    green_left_align_style = Style(
        name=green_left_align_style_name, family="table-cell"
    )
    green_left_align_style.addElement(TableCellProperties(backgroundcolor="#dde8cb"))
    green_left_align_style.addElement(ParagraphProperties(textalign="left"))
    doc.styles.addElement(green_left_align_style)

    green_center_align_style_name = "GreenCenterAlign"
    green_center_align_style = Style(
        name=green_center_align_style_name, family="table-cell"
    )
    green_center_align_style.addElement(TableCellProperties(backgroundcolor="#dde8cb"))
    green_center_align_style.addElement(ParagraphProperties(textalign="center"))
    doc.styles.addElement(green_center_align_style)

    def make_cell(
        content,
        formula=None,
        value_type="string",
        value=None,
        bg_style=None,
        align_style=None,
    ):
        cell = TableCell()

        if formula:
            cell.setAttribute("formula", formula)
            cell.setAttribute("valuetype", value_type)
            if value is not None:
                cell.setAttribute("value", str(value))
        elif value is not None:
            cell.setAttribute("valuetype", value_type)
            cell.setAttribute("value", str(value))
        else:
            cell.setAttribute("valuetype", value_type)

        p = P(text=str(content))

        if bg_style and not align_style:
            cell.setAttribute("stylename", bg_style)
        elif align_style:
            cell.setAttribute("stylename", align_style)

        cell.addElement(p)
        return cell

    # Title row
    title_row = TableRow()
    for i in range(4):
        content = f"{title}" if i == 0 else ""
        cell = TableCell()
        cell.setAttribute("stylename", grey_bg_style_name)
        p = P(text=content)
        cell.addElement(p)
        title_row.addElement(cell)
    table.addElement(title_row)

    # Assignment rows
    start_row = 2
    for i, a in enumerate(punten, start=start_row):
        row = TableRow()
        row.addElement(make_cell(a["desc"], align_style=left_align_style_name))
        row.addElement(make_cell("", value_type="float"))
        row.addElement(make_cell("/", align_style=center_align_style_name))
        row.addElement(
            make_cell(
                a["max"],
                value_type="float",
                value=a["max"],
                align_style=left_align_style_name,
            )
        )
        table.addElement(row)

    # Totals row
    end_row = start_row + len(punten) - 1
    total_row = TableRow()

    total_row.addElement(make_cell("TOTAAL", align_style=green_left_align_style_name))

    total_row.addElement(
        make_cell(
            "",
            formula=f"of:=SUM([.B{start_row}:.B{end_row}])",
            value_type="float",
            bg_style=green_bg_style_name,
        )
    )

    total_row.addElement(make_cell("/", align_style=green_center_align_style_name))

    total_row.addElement(
        make_cell(
            "",
            formula=f"of:=SUM([.D{start_row}:.D{end_row}])",
            value_type="float",
            align_style=green_left_align_style_name,
        )
    )

    table.addElement(total_row)

    total_row_num = end_row + 1
    te_laat_row_num = end_row + 2

    # "Te laat" row
    te_laat_row = TableRow()
    te_laat_row.addElement(
        make_cell("Te laat? (-20%)", align_style=left_align_style_name)
    )
    te_laat_row.addElement(make_cell("", value_type="string"))
    te_laat_row.addElement(
        make_cell(
            "",
            formula=(f'of:=IF([.B{te_laat_row_num}]<>"";[.B{total_row_num}]*-0.2;0)'),
            value_type="float",
            align_style=left_align_style_name,
        )
    )
    te_laat_row.addElement(make_cell("", value_type="string"))
    table.addElement(te_laat_row)

    # "EINDSCORE" row
    eindscore_row = TableRow()
    eindscore_row.addElement(
        make_cell("EINDSCORE", align_style=green_left_align_style_name)
    )
    eindscore_row.addElement(
        make_cell(
            "",
            formula=f"of:=[.B{total_row_num}]+[.C{te_laat_row_num}]",
            value_type="float",
            bg_style=green_bg_style_name,
        )
    )
    eindscore_row.addElement(make_cell("/", align_style=green_center_align_style_name))
    eindscore_row.addElement(
        make_cell(
            "",
            formula=f"of:=[.D{total_row_num}]",
            value_type="float",
            align_style=green_left_align_style_name,
        )
    )
    table.addElement(eindscore_row)

    doc.spreadsheet.addElement(table)

    # Doelen section
    if doelen:
        table.addElement(TableRow())

        legend_text = " ".join(
            f"{letter}: {meaning}" for letter, meaning in DOELEN_SCALE
        )
        header_row = TableRow()
        header_row.addElement(make_cell(legend_text, bg_style=doelen_bg_style_name))
        for letter, _meaning in DOELEN_SCALE:
            header_row.addElement(make_cell(letter, bg_style=doelen_bg_style_name))
        table.addElement(header_row)

        for d in doelen:
            nr = d.get("nr", "")
            desc = d.get("desc", "")
            label = f"{nr} - {desc}" if nr else desc
            row = TableRow()
            row.addElement(make_cell(label, align_style=left_align_style_name))
            for letter, _meaning in DOELEN_SCALE:
                box = CHECKED if letter == DOELEN_DEFAULT else UNCHECKED
                row.addElement(make_cell(box, align_style=center_align_style_name))
            table.addElement(row)

    safe_student_name = student_name.replace("/", "_")
    output_file = os.path.join(
        output_folder, f"{safe_student_name} - {assignment_name}.ods"
    )
    doc.save(output_file)

    return output_file


# Create spreadsheet for each student
created_files = []
for student in args.students:
    output_file = create_spreadsheet(student, basename)
    created_files.append(output_file)
    print(
        f"{BLUE}📊 Created: {os.path.basename(output_file)}{DARK_GREY}", file=sys.stderr
    )

print()
print(
    f"Successfully created {len(created_files)} spreadsheet(s) in: {output_folder}{NC}"
)


def save_folder_to_open(folder_path):
    """Save folder path to be opened by host after container exits"""
    in_docker = Path("/.dockerenv").exists()

    if in_docker:
        with open("/tmp/maesbot_output_dir/folder", "w") as f:
            f.write(folder_path)
        print(
            f"{DARK_GREY}Folder will open automatically after script completes{NC}",
            file=sys.stderr,
        )
    else:
        try:
            subprocess.run(["xdg-open", folder_path], check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"{DARK_GREY}Path: {folder_path}{NC}", file=sys.stderr)


save_folder_to_open(output_folder)
