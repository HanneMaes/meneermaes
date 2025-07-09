# ChatGPT: https://chatgpt.com/c/686cbb15-2560-8011-89cd-24327c38c158

from odfdo import Document, Table, Row, Cell, Paragraph
import yaml

# Load the assignment data
with open("testdata/toets.yml") as f:
    assignment = yaml.safe_load(f)

# Load template
template = Document("testdata/template.odt")
body = template.body

# Create table
table = Table("Grading Table")

header = Row(cells=[ # Add header row
    Cell("Description"),
    Cell("Max Points"),
    Cell("Score")
])
table.append(header)

for part in assignment["parts"]: # Add rows from assignment parts
    row = Row(cells=[
        Cell(part["description"]),
        Cell(str(part["max_points"])),
        Cell(""),  # Empty score cell to be filled later
    ])
    table.append(row)

last_row = len(assignment["parts"]) + 1 # Add total row with formulas
total_row = Row(cells=[
    Cell("Total"),
    Cell(f"=sum([.B2:.B{last_row}])"),
    Cell(f"=sum([.C2:.C{last_row}])")
])
table.append(total_row)

# Create the title
title = Paragraph(assignment["assignment_title"])

# Add title and table
body.append(title)
body.append(table)

# Create output dir if it does not exist

# Save output
template.save("taken-en-toetsen/output/grading_database.odt")
print("✅ File saved to output/grading_database.odt")
