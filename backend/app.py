from fastapi import FastAPI, UploadFile, File, HTTPException
from backend.models.schemas import RepoAnalyzeRequest, RepoAnalyzeResponse
from backend.services.repo_parser import extract_repo_context, extract_repo_context_from_path
from backend.services.prompt_builder import build_prompt
# from app.llm_service import call_ollama
from backend.services.llm_service import generate_readme
import zipfile
import tempfile
import os


app = FastAPI()

@app.get("/health")
def health():
    return {
        "status": "OK",
        "groq": "Working"
        }


