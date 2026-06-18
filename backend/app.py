from fastapi import FastAPI, UploadFile, File, HTTPException
# from backend.models.schemas import RepoAnalyzeRequest, RepoAnalyzeResponse
# from backend.services.repo_parser import extract_repo_context, extract_repo_context_from_path
# from backend.services.prompt_builder import build_prompt
# from app.llm_service import call_ollama
from backend.services.llm_service import generate_readme
from dotenv import load_dotenv
import zipfile
import tempfile
import os


app = FastAPI()


@app.get("/")
def greet():
    return {"message": "Welcome to the Readme Generator. You can paste your github urls and add .zip files to generate readme."}

@app.get("/health")
def health():
    if not os.getenv("GROQ_API_KEY"):
        return {
            "status": "ok",
            "groq": "unreachable"
            }
    return{
        "status": "ok",
        "groq": "connected"
    }