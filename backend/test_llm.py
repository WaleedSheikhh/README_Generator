import asyncio
from services.repo_parser import repo_parse
from services.prompt_builder import build_readme_prompt

async def test_prompt_builder():
    """Test Prompt Builder in isolation"""
    print("🔧 Testing prompt_builder.py (in isolation)...\n")
    
    sample_context = """
Repository URL: https://github.com/example/project
Detected Languages: .py, .js, .toml
Directory Structure:
project/
    src/
        main.py
    README.md
Key Files Content:
--- pyproject.toml ---
[project]
name = "example"
version = "0.1.0"
"""

    # Test 1: Full prompt builder
    prompt = build_readme_prompt(
        repo_context=sample_context,
        selected_sections=["Features", "Installation", "Usage", "Tech Stack"],
        custom_instructions="Make it fun and engaging for new developers.",
        project_purpose="A simple todo API built with FastAPI."
    )
    
    print("✅ build_readme_prompt() works!")
    print("First 300 characters of generated prompt:\n")
    print(prompt[:300] + "...\n")

    # # Test 2: Simple version
    # simple_prompt = build_readme_prompt(sample_context)
    # print("✅ build_simple_readme_prompt() works!\n")


async def test_parse_repo():
    """Test full pipeline"""
    print("🧪 Testing full parse_repo() with Prompt Builder...\n")
    
    repo_url = "https://github.com/tiangolo/fastapi"
    
    try:
        result = await repo_parse(
            repo_url=repo_url,
            prompt="Target Python developers. Keep it modern and clean.",
            selected_sections=[
                "Project Title & Tagline",
                "Description",
                "Features",
                "Tech Stack",
                "Installation",
                "Usage",
                "License"
            ]
        )
        
        print("✅ Full parse_repo() + Prompt Builder Successful!\n")
        print("=" * 80)
        print(result[:800] + "\n... (truncated)")
        print("=" * 80)
        
        with open("test_generated_readme.md", "w", encoding="utf-8") as f:
            f.write(result)
        print("📁 Saved full README to: test_generated_readme.md")
        
    except Exception as e:
        print(f"❌ Error: {e}")


async def main():
    await test_prompt_builder()
    print("\n" + "="*80 + "\n")
    await test_parse_repo()


if __name__ == "__main__":
    asyncio.run(main())