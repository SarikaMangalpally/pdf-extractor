import pdfplumber
from pdf2image import convert_from_bytes
from PIL import Image
import pytesseract
from io import BytesIO

def extract_text_from_page(page) -> list:
    extracted_data = []
    sections = page.extract_words()
    for word in sections:
        extracted_data.append({
            "text": word['text'],
            "bbox": [word['x0'], word['top'], word['x1'], word['bottom']]
        })
    return extracted_data

def perform_ocr_on_page(image):
    extracted_data = []
    ocr_result = pytesseract.image_to_data(image.original, output_type=pytesseract.Output.DICT)
    for i in range(len(ocr_result['text'])):
        if ocr_result['text'][i].strip():
            extracted_data.append({
                "text": ocr_result['text'][i],
                "bbox": [ocr_result['left'][i], ocr_result['top'][i],
                          ocr_result['left'][i] + ocr_result['width'][i],
                          ocr_result['top'][i] + ocr_result['height'][i]]
            })
    return extracted_data
    
def extract_text_from_pdf(pdf_content: bytes):
    text_and_bboxes = []
    with pdfplumber.open(BytesIO(pdf_content)) as pdf_file:
        for page_number, page in enumerate(pdf_file.pages, start=1):
            section_data = {
                "page_number": page_number,
                "sections": []
            }
            current_section = {
                "text_and_bboxes": extract_text_from_page(page)
            }
            image = page.to_image()
            current_section['text_and_bboxes'].extend(perform_ocr_on_page(image))
            section_data["sections"].append(current_section)
            text_and_bboxes.append(section_data)
    return text_and_bboxes


def extract_text_from_images(pdf_content: bytes):
    text_and_bboxes = []
    images = convert_from_bytes(pdf_content)
    for page_number, image in enumerate(images, start=1):
        section_data = {"page_number": page_number, "sections": []}
        current_section = {"text_and_bboxes": perform_ocr_on_page(image)}
        section_data["sections"].append(current_section)
        text_and_bboxes.append(section_data)
    return text_and_bboxes
