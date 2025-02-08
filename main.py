from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from pdf_downloader import download_pdf
from text_extractor import extract_text_from_pdf, extract_text_from_images

# import requests
# import pdfplumber
# import pytesseract
# from pdf2image import convert_from_bytes
# from io import BytesIO

app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Model
class PDFRequest(BaseModel):
    pdf_url: HttpUrl  # Changed from 'url' to 'pdf_url'

class PDFResponse(BaseModel):
    text: str
    bbox: list[float]

# API Endpoint
@app.get("/")
async def home_page_text():
    return {"msg": "Welcome to PDF Extractor API"}

# @app.post("/extract")
# async def extract_pdf_text(request: PDFRequest):
#     try:
#         pdf_content = download_pdf(str(request.pdf_url))
#         text_and_bboxes = []

#         with pdfplumber.open(BytesIO(pdf_content)) as pdf_file:
#             for page_number, page in enumerate(pdf_file.pages, start=1):
#                 sections = page.extract_words()
#                 section_data = {
#                     "page_number": page_number,
#                     "sections": []
#                 }
#                 current_section = {
#                     "text_and_bboxes": []
#                 }
            
#                 for word in sections:
#                     current_section["text_and_bboxes"].append({
#                         "text": word['text'],
#                         "bbox": [word['x0'], word['top'], word['x1'], word['bottom']]
#                     })
            
#                 image = page.to_image()
#                 ocr_result = pytesseract.image_to_data(image.original, output_type=pytesseract.Output.DICT)
#                 for i in range(len(ocr_result['text'])):
#                     if ocr_result['text'][i].strip():
#                         current_section["text_and_bboxes"].append({
#                             "text": ocr_result['text'][i],
#                             "bbox": [ocr_result['left'][i], ocr_result['top'][i], ocr_result['width'][i], ocr_result['height'][i]]
#                         })
#                 section_data["sections"].append(current_section)
#                 text_and_bboxes.append(section_data)

#         if not text_and_bboxes:
#             images = convert_from_bytes(pdf_content)
#             for page_number, image in enumerate(images, start=1):
#                 ocr_result = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
#                 section_data = {
#                     "page_number": page_number,
#                     "sections": []
#                 }
#                 current_section = {
#                     "text_and_bboxes": []
#                 }   
#                 for i in range(len(ocr_result['text'])):
#                     if ocr_result['text'][i].strip():
#                         current_section["text_and_bboxes"].append({
#                             "text": ocr_result['text'][i],
#                             "bbox": [ocr_result['left'][i], ocr_result['top'][i], ocr_result['width'][i], ocr_result['height'][i]]
#                         })
#                 section_data["sections"].append(current_section)
#                 text_and_bboxes.append(section_data)

#         return {"data": text_and_bboxes, "status": "success"}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail="Invalid PDF URL")

# def post_process_text_with_LLM(text: str):
#     # Post-process text using Language Model
#     return text

# # if __name__ == "__main__":
# #     uvicorn.run(app, host="0.0.0.0", port=8000)

@app.post("/extract")
async def extract_pdf_to_text(request: PDFRequest):
    try:
        pdf_content = download_pdf(request.pdf_url)
        text_and_bboxes = extract_text_from_pdf(pdf_content)
        if not text_and_bboxes:
            text_and_bboxes = extract_text_from_images(pdf_content)
        return {"data": text_and_bboxes, "status": "success"}
    except requests.RequestException:
        raise HTTPException(status_code=400, detail="Invalid PDF URL")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
