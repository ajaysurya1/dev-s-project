import fitz
from docx import Document
import pandas
from PIL import Image
import pytesseract

def extract_text_from_pdf(file_path):
    text = ""
    pdf_document = fitz.open(file_path)
    for page in pdf_document:
        text = text + page.get_text()
    pdf_document.close()
    return text

def extract_text_from_csv(file_path):
    dataframe = pandas.read_csv(file_path)
    return dataframe.to_string(index=False)


def extract_text_from_docx(file_path):
    document = Document(file_path)
    paragraph_list = []
    for paragraph in document.paragraphs:
        paragraph_list.append(paragraph.text)
    return "/n".join(paragraph_list)

def extract_text_from_text(file_path):
    with open(file_path, 'r', encoding = "UTF-8") as file:
        return file.read()
    
def extract_text_from_image(file_path):
    image = Image.open(file_path)
    return pytesseract.image_to_string(image)

def extract_text(file_path, file_type):
    if file_type == "pdf":
        return extract_text_from_pdf(file_path)
    elif file_type == "csv":
        return extract_text_from_csv(file_path)
    elif file_type == "docx":
        return extract_text_from_docx(file_path)
    elif file_type == "txt":
        return extract_text_from_text(file_path)
    elif file_type == "jpeg" or file_type == "png" or file_type == "jpg" or file_type == "png":
        return extract_text_from_image(file_path)
    else:
        raise ValueError("File Type not supported")
