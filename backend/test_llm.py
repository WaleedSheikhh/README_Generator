import asyncio
from services.llm_service import generate_readme

print("Script started")

async def generate_text():

    # print("Script Started..\n")
    prompt = "Write a haiku about coding"

    print("Calling generate_readme...\n")
    result = await generate_readme(prompt)
    print("Got result:", result)

    print(result)


if __name__ == "__main__":
    asyncio.run(generate_text())