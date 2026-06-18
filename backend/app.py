from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from backend.services.repo_parser import repo_parse
from backend.models.schemas import RepoReadmeRequest, RepoReadmeResponse
from dotenv import load_dotenv
import zipfile
import tempfile
import os
import shutil
from typing import Optional
import json

load_dotenv()
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/llama-4-scout-17b-16e-instruct")

app = FastAPI()


@app.get("/")
def greet():
    return {"message": "Welcome to the Readme Generator. You can paste your github urls and add .zip files to generate readme."}


@app.get("/health")
def health():
    if not os.getenv("GROQ_API_KEY"):
        return {"status": "ok", "groq": "unreachable"}
    return {"status": "ok", "groq": "connected"}


@app.post("/generate", response_model=RepoReadmeResponse)
async def generate_readme_from_url(request: RepoReadmeRequest):
    """Generate a professional README.md from a GitHub repository."""
    try:
        markdown_content = await repo_parse(
            repo_url=str(request.repo_url),
            prompt=request.prompt,
            selected_sections=request.selected_sections
        )
        return RepoReadmeResponse(
            markdown=markdown_content,
            model_used=request.model_name or MODEL_NAME,
            tokens_used=None,
            status="success"
        )

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate README: {str(e)}")


@app.post("/uploadZIPfile", response_model=RepoReadmeResponse)
async def generate_from_zip(
    file: UploadFile = File(...),
    prompt: Optional[str] = Form(default=None),
    selected_sections: Optional[str] = Form(default=None)  # JSON string
):
    """Generate README from uploaded .zip file."""
    if not file.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="Only .zip files are allowed")

    # Parse selected_sections from JSON string if provided
    # e.g. user passes: ["Features", "Installation", "Usage"]
    parsed_sections = None
    if selected_sections:
        try:
            parsed_sections = json.loads(selected_sections)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="selected_sections must be a valid JSON array string")

    temp_dir = None
    try:
        temp_dir = tempfile.mkdtemp(prefix="upload_")
        zip_path = os.path.join(temp_dir, file.filename)

        with open(zip_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        extract_path = os.path.join(temp_dir, "extracted")
        os.makedirs(extract_path, exist_ok=True)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

        markdown = await repo_parse(
            repo_url=None,
            local_path=extract_path,
            prompt=prompt,
            selected_sections=parsed_sections
        )
        return RepoReadmeResponse(
            markdown=markdown,
            model_used=MODEL_NAME,
            tokens_used=None,
            status="success"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process zip file: {str(e)}")

    finally:
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)