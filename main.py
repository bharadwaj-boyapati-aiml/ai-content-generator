import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import google.generativeai as genai

# Replace with your actual Gemini API Key
GOOGLE_API_KEY = "AIzaSyAQ_-WVo3-GXS0wdeNFsJ6-vdw2lNNQ9os"
genai.configure(api_key=GOOGLE_API_KEY)

# Load Gemini model
model = genai.GenerativeModel("gemini-pro")

# Initialize FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Define request model
class Prompt(BaseModel):
    prompt: str

# Serve the homepage
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# AI content generation endpoint
@app.post("/generate")
async def generate_text(prompt: Prompt):
    try:
        print("Received prompt:", prompt.prompt)  # Debug log
        response = model.generate_content(prompt.prompt)
        print("Gemini response:", response.text)  # Debug log
        return {"content": response.text}
    except Exception as e:
        print("Error:", str(e))  # Debug log
        return JSONResponse(status_code=500, content={"error": str(e)})
