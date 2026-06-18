import asyncio
from services.repo_parser import repo_parse

async def main():
    repo_url = "https://github.com/tiangolo/fastapi"
    
    print("🧪 Testing parse_repo with FastAPI repo...\n")
    
    try:
        result = await repo_parse(repo_url)
        print("✅ Success! Generated README:\n")
        print(result)
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())