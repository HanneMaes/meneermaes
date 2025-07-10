# ChatGPT: https://chatgpt.com/c/686cbb15-2560-8011-89cd-24327c38c158
# Claude: https://claude.ai/chat/cfef859e-f0c6-44e6-9e45-8678d8f9080a

from odfdo import Document, Table, Row, Cell, Paragraph, Span, Style
import yaml
import os

###########################################################################################
# FUNCTIONS

def make_cell(content):
    para = Paragraph()
    if isinstance(content, str):
        para.append(content)
    elif isinstance(content, list):
        for part in content:
            if isinstance(part, str):
                para.append(part)
            else:
                para.append(part)
    else:
        raise TypeError("Unsupported content type for make_cell")
    cell = Cell()
    cell.append(para)
    return cell

def make_bold_span(text):
    return Span(text, style="BoldDirect")

def parse_markdown_to_odf(text):
    # Simple bold parsing with **
    parts = text.split("**")
    result = []
    for i, part in enumerate(parts):
        if i % 2 == 0:
            result.append(part)
        else:
            result.append(make_bold_span(part))
    return result

###########################################################################################
# SCRIPT

# Load the assignment data
with open("testdata/toets.yml") as f:
    assignment = yaml.safe_load(f)

# Load template
template = Document("testdata/template.odt")
body = template.body

# Create and add bold style if not present
bold_style = Style(name="BoldDirect", family="text")
bold_style.set_properties({"fo:font-weight": "bold"})
template.insert_style(bold_style)

# Create table
table = Table("Grading Table")

# Header row
header = Row(cells=[
    make_cell("Description"),
    make_cell("Score"),
    make_cell("/"),
    make_cell("Max Points")
])
table.append(header)

# Add data rows
for part in assignment["parts"]:
    row = Row()
    desc_parts = parse_markdown_to_odf(part["description"])
    row.append(make_cell(desc_parts))
    row.append(make_cell(""))  # Score blank cell
    row.append(make_cell("/"))
    row.append(make_cell(str(part["max_points"])))
    table.append(row)

# Total row with formulas
last_row = len(assignment["parts"]) + 1  # +1 for header row

total_row = Row()

# Total label cell
total_row.append(make_cell("Total"))

# Formula cell for total score (column B)
total_score_cell = Cell()
formula_score = f"of:=SUM([.B2:.B{last_row}])"
total_score_cell.set_attribute("table:formula", formula_score)
total_score_cell.set_value_and_type("0", "float")
total_score_cell.append(Paragraph("0"))
total_row.append(total_score_cell)

# Empty cell for slash
total_row.append(make_cell(""))

# Formula cell for max points (column D)
total_max_cell = Cell()
formula_max = f"of:=SUM([.D2:.D{last_row}])"
total_max_cell.set_attribute("table:formula", formula_max)
total_max_cell.set_value_and_type("0", "float")
total_max_cell.append(Paragraph("0"))
total_row.append(total_max_cell)

table.append(total_row)

# Title paragraph
title = Paragraph(assignment["assignment_title"], style="Heading_20_1")

# Append title and table to body
body.append(title)
body.append(table)

# Create output directory if not exists
output_dir = "taken-en-toetsen/output"
os.makedirs(output_dir, exist_ok=True)

# Save output
output_file = os.path.join(output_dir, "grading_database.odt")
template.save(output_file)

print()
print(f"✅ File saved to {output_file}")
