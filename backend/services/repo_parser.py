import os
import tempfile
import shutil
from pathlib import Path
from git import Repo
from groq import AsyncGroq
from dotenv import load_dotenv
from typing import Optional, List

from .llm_service import client, MODEL
from .prompt_builder import build_readme_prompt

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


async def repo_parse(
    repo_url: Optional[str] = None,
    local_path: Optional[str] = None,
    prompt: Optional[str] = None,
    selected_sections: Optional[List[str]] = None
) -> str:
    
    if not repo_url and not local_path:
        raise ValueError("Either repo_url or local_path must be provided.")

    temp_dir = None
    try:
        if repo_url:
            temp_dir = tempfile.mkdtemp(prefix="repo_")
            print(f"Cloning the Repo {repo_url}")
            Repo.clone_from(repo_url, temp_dir)
            working_dir = temp_dir
        else:
            working_dir = local_path
            print(f"Using local path: {working_dir}")

        # Build directory structure
        structure = []
        for root, dirs, files in os.walk(working_dir):
            level = root.replace(working_dir, "").count(os.sep)
            indent = "    " * level
            structure.append(f"{indent}{os.path.basename(root)}/")
            sub_indent = "    " * (level + 1)
            for f in sorted(files):
                structure.append(f"{sub_indent}{f}")

        structure_str = "\n".join(structure[:200])

        # Read key files
        content_summary = []
        for key_file in KEY_FILES:
            file_path = None
            for root, _, files in os.walk(working_dir):
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

        project_name = "Unknown"
        for root, _, files in os.walk(working_dir):
            if "pyproject.toml" in files:
                with open(os.path.join(root, "pyproject.toml")) as f:
                    for line in f:
                        if line.startswith("name"):
                            project_name = line.split("=")[1].strip().strip('"')
                            break
            if "package.json" in files:
                import json
                with open(os.path.join(root, "package.json")) as f:
                    data = json.load(f)
                    project_name = data.get("name", project_name)


        extensions = set()
        for root, _, files in os.walk(working_dir):
            for file in files:
                ext = Path(file).suffix.lower()
                if ext:
                    extensions.add(ext)
        languages = ", ".join(sorted(extensions)) if extensions else "Unknown"


        full_context = f"""
Repository URL: {repo_url or "Uploaded ZIP"}
Detected Languages: {languages}

Directory Structure:
{structure_str}

Key Files Content:
{"".join(content_summary)}
"""

        final_prompt = build_readme_prompt(
            repo_context=full_context,
            selected_sections=selected_sections,
            custom_instructions=prompt,
            project_purpose=None
        )

        response = await client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert technical writer who creates modern, original README files. Never copy content verbatim from existing README files. Never include full license text — only mention the license name. Always use the actual repository name and real details found in the code." 
                },
                {
                    "role": "user",
                    "content": final_prompt
                }
            ],
            temperature=0.7,
            max_tokens=4000,
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