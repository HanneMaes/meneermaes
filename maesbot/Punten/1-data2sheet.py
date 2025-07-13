import os
import yaml
import argparse
from odf.opendocument import OpenDocumentSpreadsheet
from odf.style import Style, TableColumnProperties, TableCellProperties, ParagraphProperties
from odf.table import Table, TableColumn, TableRow, TableCell
from odf.text import P

# Parse args
parser = argparse.ArgumentParser()
parser.add_argument('--input', required=True, help="Path to input YAML file")
parser.add_argument('--output', required=True, help="Path to output directory")
args = parser.parse_args()

# Load YAML input once
with open(args.input) as f:
    data = yaml.safe_load(f)

print(f"Loaded input YAML from {args.input}")

# Extract base name for output file/folder
basename = os.path.splitext(os.path.basename(args.input))[0]

# Make sure output directory exists
os.makedirs(args.output, exist_ok=True)

title = data.get("title", "Assignment")
assignments = data.get("assignments", [])  # Fixed typo here

output_folder = os.path.join(args.output, basename)
os.makedirs(output_folder, exist_ok=True)
output_file = os.path.join(output_folder, f"{basename}.ods")

# Create spreadsheet
doc = OpenDocumentSpreadsheet()
table = Table(name="Grading")

# Column widths
for width in ("15cm", "0.6cm", "0.3cm", "0.6cm"):
    col_style = Style(name=f"col_{width}", family="table-column")
    col_style.addElement(TableColumnProperties(columnwidth=width))
    doc.automaticstyles.addElement(col_style)
    table.addElement(TableColumn(stylename=col_style.name))

# Define styles (only names are passed to cells)
grey_bg_style = Style(name="GreyBackground", family="table-cell")
grey_bg_style.addElement(TableCellProperties(backgroundcolor="#e5e5e5"))  # Light gray background
doc.styles.addElement(grey_bg_style)

green_bg_style = Style(name="GreenBackground", family="table-cell")
green_bg_style.addElement(TableCellProperties(backgroundcolor="#dde8cb"))  # Light green background
doc.styles.addElement(green_bg_style)

center_align_style = Style(name="CenterAlign", family="table-cell")
center_align_style.addElement(TableCellProperties())
center_align_style.addElement(ParagraphProperties(textalign="center"))
doc.styles.addElement(center_align_style)

left_align_style = Style(name="LeftAlign", family="table-cell")
left_align_style.addElement(TableCellProperties())
left_align_style.addElement(ParagraphProperties(textalign="left"))
doc.styles.addElement(left_align_style)

green_left_align_style = Style(name="GreenLeftAlign", family="table-cell")
green_left_align_style.addElement(TableCellProperties(backgroundcolor="#dde8cb"))
green_left_align_style.addElement(ParagraphProperties(textalign="left"))
doc.styles.addElement(green_left_align_style)

green_center_align_style = Style(name="GreenCenterAlign", family="table-cell")
green_center_align_style.addElement(TableCellProperties(backgroundcolor="#dde8cb"))
green_center_align_style.addElement(ParagraphProperties(textalign="center"))
doc.styles.addElement(green_center_align_style)

def make_cell(content, formula=None, value_type="string", value=None, bg_style=None, align_style=None):
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

# Title row with gray background
title_row = TableRow()
for i in range(4):
    content = title if i == 0 else ""
    cell = TableCell()
    cell.setAttribute("stylename", grey_bg_style.name)
    p = P(text=content)
    cell.addElement(p)
    title_row.addElement(cell)
table.addElement(title_row)

start_row = 2
for i, a in enumerate(assignments, start=start_row):
    row = TableRow()
    row.addElement(make_cell(a["desc"], align_style=left_align_style.name))
    row.addElement(make_cell("", value_type="float"))
    row.addElement(make_cell("/", align_style=center_align_style.name))
    row.addElement(make_cell(a["max"], value_type="float", value=a["max"], align_style=left_align_style.name))
    table.addElement(row)

end_row = start_row + len(assignments) - 1
total_row = TableRow()
total_row.addElement(make_cell("TOTAAL", align_style=green_left_align_style.name))
total_row.addElement(
    make_cell(
        "",
        formula=f"of:=SUM([.B{start_row}:.B{end_row}])",
        value_type="float",
        value=0,
        bg_style=green_bg_style.name,
    )
)
total_row.addElement(make_cell("/", align_style=green_center_align_style.name))
total_row.addElement(
    make_cell(
        "",
        formula=f"of:=SUM([.D{start_row}:.D{end_row}])",
        value_type="float",
        value=0,
        align_style=green_left_align_style.name,
    )
)
table.addElement(total_row)

doc.spreadsheet.addElement(table)
doc.save(output_file)

print(f"\033[92m  📗 Sheet: {output_file}\033[0m")
