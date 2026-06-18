import httpx, os
from dotenv import load_dotenv
from groq import AsyncGroq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("MODEL_NAME")

client = AsyncGroq(api_key= GROQ_API_KEY)

async def generate_readme(prompt: str, model: str = "meta-llama/llama-4-scout-17b-16e-instruct") -> str:

    if not os.getenv("GROQ_API_KEY"):
        raise ValueError("GROQ key not found in .env file.")
    
    try:
        response = await client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert technical writer. Generate high-quality, professional README content."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=2000,
        )
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        raise RuntimeError(f"Failed to generate Readme: {str(e)}")