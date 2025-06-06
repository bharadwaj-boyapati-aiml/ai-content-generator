import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import google.generativeai as genai

# Set your Gemini API key
GOOGLE_API_KEY = "AIzaSyAQ_-WVo3-GXS0wdeNFsJ6-vdw2lNNQ9os"
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-pro")

# FastAPI app
app = FastAPI()

# CORS and Static Files
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Request schema
class Prompt(BaseModel):
    prompt: str

@app.post("/generate")
async def generate_text(prompt: Prompt):
    try:
        response = model.generate_content(prompt.prompt)
        return {"content": response.text}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/", response_class=JSONResponse)
async def root(request: Request):
    with open("templates/index.html", "r") as f:
        return HTMLResponse(content=f.read())
