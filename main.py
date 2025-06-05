import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import google.generativeai as genai
from PIL import Image

# Configure Gemini API
GOOGLE_API_KEY = "AIzaSyAasJyvMkMPNalF4hQ0-9_x_Sf_D-LX5M0"
genai.configure(api_key=GOOGLE_API_KEY)

config = {
    'temperature': 0.7,
    'top_k': 20,
    'top_p': 0.9,
    'max_output_tokens': 4096,
    'stop_sequences': ['<|END]|>']
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="models/gemini-1.5-flash",
    generation_config=config,
    safety_settings=safety_settings
)

app = FastAPI()

# Enable CORS (important for frontend communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Static & templating config
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# UI
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Request model
class ContentRequest(BaseModel):
    topic: str
    content_type: str


# API Endpoint
@app.post("/generate")
def generate_content(req: ContentRequest):
    prompt = f"Write a high-quality, engaging {req.content_type} post about: {req.topic}"
    try:
        response = model.generate_content(prompt)
        return {"generated_content": response.text.strip()}
    except Exception as e:
        return JSONResponse(content={"generated_content": f"Error: {str(e)}"}, status_code=500)