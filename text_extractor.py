import os
import logging
from typing import Optional
import PyPDF2
import docx2txt
from werkzeug.utils import secure_filename

def extract_text_from_file(file_path: str, filename: str) -> Optional[str]:
    """
    Extract text from uploaded resume file (PDF, DOC, DOCX)
    """
    try:
        # Get file extension
        _, ext = os.path.splitext(filename.lower())
        
        if ext == '.pdf':
            return extract_text_from_pdf(file_path)
        elif ext in ['.doc', '.docx']:
            return extract_text_from_docx(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")
            
    except Exception as e:
        logging.error(f"Failed to extract text from {filename}: {e}")
        return None

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from PDF file using PyPDF2
    """
    text = ""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
                
        return text.strip()
    except Exception as e:
        logging.error(f"Failed to extract text from PDF: {e}")
        raise

def extract_text_from_docx(file_path: str) -> str:
    """
    Extract text from DOC/DOCX file using docx2txt
    """
    try:
        text = docx2txt.process(file_path)
        return text.strip() if text else ""
    except Exception as e:
        logging.error(f"Failed to extract text from DOCX: {e}")
        raise

def is_allowed_file(filename: str) -> bool:
    """
    Check if uploaded file has an allowed extension
    """
    allowed_extensions = {'.pdf', '.doc', '.docx'}
    _, ext = os.path.splitext(filename.lower())
    return ext in allowed_extensions

def save_uploaded_file(file, upload_folder: str) -> Optional[str]:
    """
    Save uploaded file securely and return the file path
    """
    try:
        if file.filename == '':
            return None
            
        if not is_allowed_file(file.filename):
            raise ValueError("File type not allowed")
            
        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_folder, filename)
        
        # Ensure unique filename
        counter = 1
        base_name, ext = os.path.splitext(filename)
        while os.path.exists(file_path):
            filename = f"{base_name}_{counter}{ext}"
            file_path = os.path.join(upload_folder, filename)
            counter += 1
            
        file.save(file_path)
        return file_path
        
    except Exception as e:
        logging.error(f"Failed to save uploaded file: {e}")
        return None
