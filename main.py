from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pydantic import BaseModel
import pytesseract
from PIL import Image
import fitz  # PyMuPDF
import openai
import io
from dotenv import load_dotenv
import os

# Initialize FastAPI app
app = FastAPI()

# Allow frontend to access this API (update origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_text_from_image(file: UploadFile):
    image = Image.open(file.file)
    return pytesseract.image_to_string(image)

def extract_text_from_pdf(file: UploadFile):
    pdf_bytes = file.file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

class TextRequest(BaseModel):
    input_text: str

@app.post("/generate-content/")
async def generate_content(
    file: Optional[UploadFile] = File(None),
    input_text: Optional[str] = Form(None),
    file_type: Optional[str] = Form(None)
):
    if file:
        if file_type == "image":
            extracted_text = extract_text_from_image(file)
        elif file_type == "pdf":
            extracted_text = extract_text_from_pdf(file)
        else:
            return {"error": "Unsupported file type"}
    elif input_text:
        extracted_text = input_text
    else:
        return {"error": "No input provided"}

    # Use ChatGPT (GPT-4 or GPT-3.5) to generate content
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Or "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "You're a helpful AI content creator."},
            {"role": "user", "content": f"Generate engaging marketing content based on this:\n\n{extracted_text}"}
        ]
    )

    result = response['choices'][0]['message']['content']
    return {"generated_content": result}