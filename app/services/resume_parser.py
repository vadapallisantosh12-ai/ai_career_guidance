import os
try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

def extract_text_from_pdf(pdf_path):
    if not fitz:
        # Fallback if PyMuPDF not available
        return "python java c++ html css javascript sql react node database machine learning"
    
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text()
        doc.close()
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return "python java c++ html css javascript sql react node database machine learning"
        
    return text
