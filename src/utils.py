from PyPDF2 import PdfReader
import os

def extract_text_from_pdf(pdf_path):
    """
    Извлекает текст из одного PDF-файла.
    """
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_folder(folder_path):
    """
    Извлекает текст из всех PDF-файлов в папке.
    """
    combined_text = ""
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            combined_text += extract_text_from_pdf(file_path) + "\n"
    return combined_text