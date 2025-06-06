import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import google.generativeai as genai

# Your actual Gemini API Key
GOOGLE_API_KEY = "AIzaSyAQ_-WVo3-GXS0wdeNFsJ6-vdw2lNNQ9os"
genai.configure(api_key=GOOGLE_API_KEY)

# Generation parameters
config = {
    'temperature': 0.7,
    'top_k': 20,
    'top_p': 0.9,
    'max_output_tokens': 4096,
    'stop_sequences': ['<|END|>']
}

# Safety filters
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# Initialize Gemini model with config and safety settings
model = genai.GenerativeModel(
    model_name="models/gemini-1.5-flash",
    generation_config=config,
    safety_settings=safety_settings
)

# FastAPI setup
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set specific origin(s) in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static and Templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Pydantic model
class Prompt(BaseModel):
    prompt: str

# Home route
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# AI Generation endpoint
@app.post("/generate")
async def generate_text(prompt: Prompt):
    try:
        print("Received prompt:", prompt.prompt)  # Debug

        # Format the input
        formatted_prompt = (
        f"You are a professional social media content writer. "
        f"Generate a highly engaging, visually compelling content for social media post on the topic: '{prompt.prompt}'.\n"
        f"- Use an enthusiastic tone.\n"
        f"- Write at least 200 words with some interesting emojis.\n"
        f"- Begin with a powerful hook.\n"
        f"- Include 3-5 trending hashtags related to the topic.\n"
        f"- End with a strong call-to-action (CTA).\n"
        f"- Ensure the post is suitable for Instagram.\n"
        f"- Format it cleanly for copy-paste readiness.\n"
)
        # Generate response from Gemini
        response = model.generate_content(formatted_prompt)
        print("Gemini response:", response.text)  # Debug

        return {"content": response.text}

    except Exception as e:
        print("Error:", str(e))  # Debug
        return JSONResponse(status_code=500, content={"error": str(e)})
