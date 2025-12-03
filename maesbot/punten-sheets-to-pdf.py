import os  # For file system operations (paths, directories)
import argparse  # For parsing command-line arguments
import subprocess  # For running external commands (opening file manager)
import zipfile  # For reading ODS and ODT files (they are ZIP archives)
import xml.etree.ElementTree as ET  # For parsing XML content
import tempfile  # For temporary files during conversion
import shutil  # For file operations

# Template location
TEMPLATE_PATH = "/home/hanne/Documents/Nextcloud/School/maesbot-private-data/Punten/Templates/Taak-toets.odt"

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Extract points from ODS files and create PDF reports using ODT template")
parser.add_argument('--input', required=True, help="Directory containing ODS files")
parser.add_argument('--output', required=True, help="Path to output directory for PDFs")
args = parser.parse_args()

# Ensure output directory exists
os.makedirs(args.output, exist_ok=True)

def extract_data_from_ods(ods_file_path):
    """
    Extract grading data from an ODS spreadsheet file.
    
    Args:
        ods_file_path: Path to the .ods file
    
    Returns:
        Dictionary containing student name, assignments, and totals
    """
    try:
        # ODS files are ZIP archives containing XML files
        with zipfile.ZipFile(ods_file_path, 'r') as zip_file:
            # Read the content.xml file which contains the actual data
            content_xml = zip_file.read('content.xml')
            
        # Parse the XML content
        root = ET.fromstring(content_xml)
        
        # Define XML namespaces used in ODS files
        namespaces = {
            'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
            'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
            'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'
        }
        
        # Find the table element
        table_elem = root.find('.//table:table', namespaces)
        if table_elem is None:
            print(f"❌ No table found in {ods_file_path}")
            return None
            
        rows = table_elem.findall('.//table:table-row', namespaces)
        if len(rows) < 2:
            print(f"❌ Not enough rows in {ods_file_path}")
            return None
        
        # Extract student name from title row (first row, first cell)
        title_cell = rows[0].find('.//text:p', namespaces)
        title_text = title_cell.text if title_cell is not None and title_cell.text else "Unknown"
        
        # Extract student name from title (assumes format "Assignment - Student Name")
        student_name = "Unknown Student"
        assignment_title = args.title
        if " - " in title_text:
            parts = title_text.split(" - ", 1)
            assignment_title = parts[0]
            student_name = parts[1]
        
        # Extract assignment data from data rows (skip first row which is title)
        assignments = []
        total_points = 0
        max_total = 0
        
        # Process each data row (excluding title and total rows)
        for row in rows[1:-1]:  # Skip first (title) and last (total) row
            cells = row.findall('.//table:table-cell', namespaces)
            if len(cells) >= 4:
                # Extract description from first cell
                desc_elem = cells[0].find('.//text:p', namespaces)
                description = desc_elem.text if desc_elem is not None and desc_elem.text else ""
                
                # Extract score from second cell
                score_elem = cells[1].find('.//text:p', namespaces)
                score_text = score_elem.text if score_elem is not None and score_elem.text else "0"
                try:
                    score = float(score_text) if score_text.strip() else 0
                except ValueError:
                    score = 0
                
                # Extract max points from fourth cell
                max_elem = cells[3].find('.//text:p', namespaces)
                max_text = max_elem.text if max_elem is not None and max_elem.text else "0"
                try:
                    max_points = float(max_text) if max_text.strip() else 0
                except ValueError:
                    max_points = 0
                
                if description.strip():  # Only add if description is not empty
                    assignments.append({
                        'description': description,
                        'score': score,
                        'max_points': max_points
                    })
                    total_points += score
                    max_total += max_points
        
        return {
            'student_name': student_name,
            'assignment_title': assignment_title,
            'assignments': assignments,
            'total_score': total_points,
            'total_max': max_total,
            'percentage': (total_points / max_total * 100) if max_total > 0 else 0
        }
        
    except Exception as e:
        print(f"❌ Error reading {ods_file_path}: {str(e)}")
        return None

def create_assignments_table_text(assignments):
    """
    Create a formatted text representation of the assignments table.
    
    Args:
        assignments: List of assignment dictionaries
        
    Returns:
        Formatted string representing the assignments table
    """
    table_text = ""
    for assignment in assignments:
        score_str = str(int(assignment['score']) if assignment['score'].is_integer() else assignment['score'])
        max_str = str(int(assignment['max_points']) if assignment['max_points'].is_integer() else assignment['max_points'])
        table_text += f"{assignment['description']}: {score_str}/{max_str}\n"
    
    return table_text.strip()

def fill_odt_template(template_path, data, output_path):
    """
    Fill an ODT template with grading data.
    
    Args:
        template_path: Path to the ODT template file
        data: Dictionary containing grading data
        output_path: Where to save the filled ODT file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Create a temporary copy of the template
        temp_odt = output_path
        shutil.copy2(template_path, temp_odt)
        
        # Open the ODT file (it's a ZIP archive)
        with zipfile.ZipFile(temp_odt, 'a') as zip_file:
            # Read content.xml
            content_xml = zip_file.read('content.xml').decode('utf-8')
            
            # Replace placeholders with actual data
            replacements = {
                '{{STUDENT_NAME}}': data['student_name'],
                '{{ASSIGNMENT_TITLE}}': data['assignment_title'],
                '{{ASSIGNMENTS_TABLE}}': create_assignments_table_text(data['assignments']),
                '{{TOTAL_SCORE}}': str(int(data['total_score']) if data['total_score'].is_integer() else data['total_score']),
                '{{TOTAL_MAX}}': str(int(data['total_max']) if data['total_max'].is_integer() else data['total_max']),
                '{{PERCENTAGE}}': f"{data['percentage']:.1f}"
            }
            
            # Perform replacements
            for placeholder, value in replacements.items():
                content_xml = content_xml.replace(placeholder, value)
            
            # Write back the modified content.xml
            # First, remove the old content.xml
            temp_files = []
            with zipfile.ZipFile(temp_odt, 'r') as read_zip:
                for item in read_zip.infolist():
                    if item.filename != 'content.xml':
                        temp_files.append((item, read_zip.read(item.filename)))
            
            # Recreate the ZIP with modified content
            with zipfile.ZipFile(temp_odt, 'w', zipfile.ZIP_DEFLATED) as write_zip:
                # Write all files except content.xml
                for item_info, item_data in temp_files:
                    write_zip.writestr(item_info, item_data)
                
                # Write modified content.xml
                write_zip.writestr('content.xml', content_xml.encode('utf-8'))
        
        return True
        
    except Exception as e:
        print(f"❌ Error filling ODT template: {str(e)}")
        return False

def convert_odt_to_pdf(odt_path, pdf_path):
    """
    Convert ODT file to PDF using LibreOffice.
    
    Args:
        odt_path: Path to the ODT file
        pdf_path: Path where PDF should be saved
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Get directory for output
        output_dir = os.path.dirname(pdf_path)
        
        # Use LibreOffice to convert ODT to PDF
        cmd = [
            'libreoffice',
            '--headless',  # Run without GUI
            '--convert-to', 'pdf',
            '--outdir', output_dir,
            odt_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            # LibreOffice creates PDF with same base name as ODT
            base_name = os.path.splitext(os.path.basename(odt_path))[0]
            generated_pdf = os.path.join(output_dir, f"{base_name}.pdf")
            
            # Rename to desired name if different
            if generated_pdf != pdf_path:
                if os.path.exists(generated_pdf):
                    shutil.move(generated_pdf, pdf_path)
            
            return os.path.exists(pdf_path)
        else:
            print(f"❌ LibreOffice conversion failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error converting to PDF: {str(e)}")
        return False

def main():
    """Main function to process all ODS files and create PDF reports."""
    
    # Check if template exists
    if not os.path.exists(TEMPLATE_PATH):
        print(f"❌ Template file not found: {TEMPLATE_PATH}")
        print("Please update the TEMPLATE_PATH variable in the script")
        return
    
    print(f"Using template: {TEMPLATE_PATH}")
    print(f"Processing ODS files from: {args.input}")
    print(f"Output directory: {args.output}")
    print()
    
    # Find all ODS files in input directory
    ods_files = []
    for file in os.listdir(args.input):
        if file.endswith('.ods'):
            ods_files.append(os.path.join(args.input, file))
    
    if not ods_files:
        print(f"❌ No ODS files found in {args.input}")
        return
    
    print(f"Found {len(ods_files)} ODS file(s)")
    
    # Process each ODS file
    created_pdfs = []
    for ods_file in ods_files:
        print(f"Processing: {os.path.basename(ods_file)}")
        
        # Extract data from ODS
        data = extract_data_from_ods(ods_file)
        if data is None:
            continue
        
        # Create output filenames
        base_name = os.path.splitext(os.path.basename(ods_file))[0]
        temp_odt_path = os.path.join(args.output, f"{base_name}_temp.odt")
        pdf_path = os.path.join(args.output, f"{base_name}.pdf")
        
        # Fill ODT template
        if not fill_odt_template(TEMPLATE_PATH, data, temp_odt_path):
            continue
        
        # Convert ODT to PDF
        if convert_odt_to_pdf(temp_odt_path, pdf_path):
            created_pdfs.append(pdf_path)
            print(f"  ✅ Created: {os.path.basename(pdf_path)}")
            
            # Clean up temporary ODT file
            try:
                os.remove(temp_odt_path)
            except:
                pass
        else:
            print(f"  ❌ Failed to create: {os.path.basename(pdf_path)}")
    
    print()
    print(f"✅ Successfully created {len(created_pdfs)} PDF report(s)")
    
    # Open output directory
    try:
        subprocess.run(["xdg-open", args.output], check=True)
        print("📂 Opened output directory")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"📁 Output directory: {args.output}")

if __name__ == "__main__":
    main()

######################################################################################################
# GUIDE

# $ python3 2-sheet2pdf.py --input "/home/hanne/Documents/Nextcloud/School/maesbot-private-data/Punten/Generated Output/5IFCW/servers" --output "/home/hanne/Documents/Nextcloud/School/maesbot-private-data/Punten/PDF Reports/"
