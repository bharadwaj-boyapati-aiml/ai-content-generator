import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import google.generativeai as genai

# Replace this with your actual Gemini API Key
GOOGLE_API_KEY = "AIzaSyAQ_-WVo3-GXS0wdeNFsJ6-vdw2lNNQ9os"
genai.configure(api_key=GOOGLE_API_KEY)

# Load the Gemini model
model = genai.GenerativeModel("gemini-pro")

# Initialize FastAPI app
app = FastAPI()

# Allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, set this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static and template directories
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Request body structure
class Prompt(BaseModel):
    prompt: str

# Home route: Serves index.html
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# API route to generate content
@app.post("/generate")
async def generate_text(prompt: Prompt):
    try:
        response = model.generate_content(prompt.prompt)
        return {"content": response.text}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
