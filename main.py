from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import pdfplumber
import pytesseract
from pdf2image import convert_from_bytes
from io import BytesIO

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
    pdf_url: str  # Changed from 'url' to 'pdf_url'

# API Endpoint
@app.get("/")
async def home_page_text():
    return {"msg": "Welcome to PDF Extractor API"}

@app.post("/extract")
async def extract_pdf_text(request: PDFRequest):
    try:
        # return {"pdf_url": request.pdf_url}  # Updated to use 'pdf_url'
        # Extract text from PDF
        pdf = requests.get(request.pdf_url)
        images = convert_from_bytes(pdf.content)
        text = ""
        for image in images:
            text += pytesseract.image_to_string(image)
        return {"text": text, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # result = extract_text_and_bboxes(request.pdf_url)
    # return {"pdf_url": request.pdf_url}
