from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from pdf_downloader import download_pdf
from text_extractor import extract_text_from_pdf, extract_text_from_images


app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class PDFRequest(BaseModel):
    pdf_url: HttpUrl  # Changed from 'url' to 'pdf_url'

class PDFResponse(BaseModel):
    text: str
    bbox: list[float]

# API Endpoint
@app.get("/")
async def home_page_text():
    return {"msg": "Welcome to PDF Extractor API"}

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