import os
import tempfile
import shutil
from pathlib import Path
from git import Repo
from groq import AsyncGroq
from dotenv import load_dotenv
from typing import Optional

from services.llm_service import client, MODEL

KEY_FILES = [

    "README.md", "README.rst", "docs/README.md",
    "CONTRIBUTING.md", "LICENSE", ".env.example", "Dockerfile",
    "pyproject.toml", "setup.py", "requirements.txt", "Pipfile",
    "main.py", "app.py", "__init__.py", "manage.py", "settings.py", "urls.py",
    "package.json", "yarn.lock", "pnpm-lock.yaml",
    "server.js", "index.js", "src/index.js", "src/index.jsx",
    "src/App.js", "src/App.jsx", "public/index.html",
    "routes/index.js", "routes/api.js", "controllers/index.js", "models/index.js",
    "db.js", "config/database.js",
    "Cargo.toml", "src/main.rs",
    "go.mod",
    "pom.xml", "build.gradle",
    "Gemfile", "Gemfile.lock", "config/routes.rb",
    "composer.json", "composer.lock", "artisan",
    "Program.cs", "Startup.cs", "*.csproj"
    
]


async def repo_parse(repo_url: str, prompt: Optional[str] = None) -> str:
    temp_dir = None
    try:
        temp_dir = tempfile.mkdtemp(prefix="repo_")
        print(f"Cloning the Repo {repo_url}")

        Repo.clone_from(repo_url, temp_dir)

        structure= []
        for root, dirs, files in os.walk(temp_dir):
            level = root.replace(temp_dir, "").count(os.sep)
            indent = "    " * level
            structure.append(f"{indent}{os.path.basename(root)}/")
            sub_indent = "    " * (level + 1)
            for f in sorted(files):
                structure.append(f"{sub_indent}{f}")

        structure_str = "\n".join(structure[:200])

        content_summary = []
        for key_file in KEY_FILES:
            file_path = None
            for root, _, files in os.walk(temp_dir):
                if key_file in files:
                    file_path = os.path.join(root, key_file)
                    break
            if file_path and os.path.exists(file_path):
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()[:200]
                        content = "".join(lines)
                        content_summary.append(f"\n--- {key_file} ---\n{content}")
                except Exception:
                    content_summary.append(f"\n--- {key_file} ---\n[Error reading file]")

            extensions = set()
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    ext = Path(file).suffix.lower()
                    if ext:
                        extensions.add(ext)
            languages = ", ".join(sorted(extensions)) if extensions else "Unknown"

            
            
            full_context = f"""
            Repository URL: {repo_url}
            Detected Languages: {languages}

            Directory Structure:
            {structure_str}

            Key Files Content:
            {"".join(content_summary)}
            """

            user_prompt = prompt or (
                "Write a professional, modern, and engaging README.md for this project. "
                "Include sections such as: Features, Installation, Usage, Tech Stack, "
                "Contributing, and License."
            )


            response = await client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert technical writer. Generate high-quality, professional README content."
                },
                {
                    "role": "user",
                    "content": f"{full_context}\n\n{user_prompt}"
                }
            ],
            temperature=0.7,
            max_tokens=2000,
            )

            return response.choices[0].message.content.strip()
        

    except Exception as e:
        error = str(e).lower()
        if "not found" in error or "repository" in error:
            raise ValueError(f"Repository not found or inaccessible: {repo_url}")
        elif "authentication" in error or "token" in error:
            raise ValueError("Private repositories are not supported yet.")
        else:
            raise RuntimeError(f"Failed to process repository: {str(e)}")
        
    finally:
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)
            print("Temporary files cleaned up.")