import sys

file_path = r'c:\kallavi-turk-skills\The-Complete-Guide-to-Building-Skill-for-Claude.pdf'
output_path = r'c:\kallavi-turk-skills\pdf_content.txt'

try:
    import fitz  # PyMuPDF
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text() + "\n"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    print("PDF read successfully with PyMuPDF.")
    sys.exit(0)
except ImportError:
    pass

try:
    import pypdf
    reader = pypdf.PdfReader(file_path)
    text = ""
    for page in reader.pages:
        t = page.extract_text()
        if t: text += t + "\n"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    print("PDF read successfully with pypdf.")
    sys.exit(0)
except ImportError:
    pass

try:
    import PyPDF2
    reader = PyPDF2.PdfReader(file_path)
    text = ""
    for page in reader.pages:
        t = page.extract_text()
        if t: text += t + "\n"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    print("PDF read successfully with PyPDF2.")
    sys.exit(0)
except ImportError:
    print("Failed to import any PDF library.")
    sys.exit(1)
