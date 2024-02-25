import zipfile
import os
import fitz  # PyMuPDF
from datetime import datetime
from reportlab.pdfgen import canvas
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_for_filename, TextLexer



# Path to the downloaded GitHub repo zip file
zip_path = 'ISMv900v103.zip'  # Update this path
extract_path = './extracted'  # Change to a specific directory

# Extract the zip file
print("Extracting zip file...")
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)
print("Extraction complete.")

# Initialize a PDF canvas
# For unique file naming
current_time = datetime.now().strftime("%Y%m%d%H%M")
output_filename = f"github_repo_review_{current_time}.pdf"
c = canvas.Canvas(output_filename, pagesize=(8.5 * 72, 11 * 72))
c.setFont("Helvetica", 10)
height = 11 * 72 - 20  # Starting height for text


def process_pdf(file_path):
    global height
    pdf_document = fitz.open(file_path)
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text = page.get_text("text")
        for line in text.split('\n'):
            c.drawString(20, height, line)
            height -= 10
            if height < 20:
                c.showPage()
                c.setFont("Helvetica", 10)
                height = 11 * 72 - 20

                
                
def process_directory(directory):
    global height
    for root, dirs, files in os.walk(directory):
        for file in files:
            print(f"Processing file: {file}")
            file_path = os.path.join(root, file)
            
            if file.endswith('.pdf'):
                print(f"Processing PDF file: {file}")
                process_pdf(file_path)
                continue  # Skip the rest of the loop to avoid reading the PDF as text
            
            # For non-PDF files, proceed to open and process
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                print(f"Warning: Could not decode {file_path}. Skipping.")
                continue

            # Determine the lexer for syntax highlighting
            try:
                lexer = get_lexer_for_filename(file_path)
            except ValueError:
                lexer = TextLexer()

            # Syntax highlight the content
            highlighted = highlight(content, lexer, HtmlFormatter(nowrap=True))

            # Add directory path and file name to PDF
            c.drawString(20, height, f"Directory: {root}")
            height -= 10
            c.drawString(20, height, f"File: {file}")
            height -= 10

            # Add content to PDF
            for line in content.split('\n'):
                c.drawString(20, height, line)
                height -= 10
                if height < 20:
                    c.showPage()
                    c.setFont("Helvetica", 10)
                    height = 11 * 72 - 20

                    
                    
                    
def process_directoryv1(directory):
    global height
    for root, dirs, files in os.walk(directory):
        for file in files:
            print(f"Processing file: {file}")
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                print(f"Warning: Could not decode {file_path}. Skipping.")
                continue

            # Determine the lexer based on the file type
            try:
                lexer = get_lexer_for_filename(file_path)
            except ValueError:
                lexer = TextLexer()
                
            if file.endswith('.pdf'):
                print(f"Processing PDF file: {file}")
                process_pdf(file_path)
                continue
                
                
            # Syntax highlight the content
            highlighted = highlight(content, lexer, HtmlFormatter(nowrap=True))

            # Add directory path and file name to PDF
            c.drawString(20, height, f"Directory: {root}")
            height -= 10
            c.drawString(20, height, f"File: {file}")
            height -= 10

            # Add content to PDF
            for line in content.split('\n'):
                c.drawString(20, height, line)
                height -= 10
                if height < 20:
                    c.showPage()
                    c.setFont("Helvetica", 10)
                    height = 11 * 72 - 20


                        
# Process the extracted directory
process_directory(extract_path)

# Finalize and save the PDF
print("Finalizing PDF...")
c.save()
print(f"PDF saved as {output_filename}.")
