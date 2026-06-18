from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List

class RepoReadmeRequest(BaseModel):

    repo_url: HttpUrl = Field(
        ...,
        desc = "List of sections to include in the README",
        example = "https://github.com/tiangolo/fastapi"
    )

    selected_sections: Optional[List[str]] = Field(
        default=None,
        description="List of sections to include in the README",
        example=["Features", "Installation", "Usage", "Tech Stack", "License"]
    )

    prompt: Optional[str] = Field(
        default=None,
        description="Custom instructions for the README generation",
        example="Make it beginner-friendly and focus on async capabilities."
    )
    
    model_name: Optional[str] = Field(
        default=None,
        description="Groq model to use (optional)",
        example="llama-3.1-8b-instant"
    )


class config():
    json_schema_extra = {
        "example": {
            "repo_url": "https://github.com/tiangolo/fastapi",
            "selected_sections": ["Features", "Installation", "Usage", "Tech Stack"],
            "prompt": "Target intermediate Python developers.",
            "model_name": "llama-3.1-8b-instant"
        }
    }

class RepoReadmeResponse(BaseModel):
    """
    Response schema after generating README.
    """
    markdown: str = Field(..., description="The generated README content in Markdown")
    
    model_used: str = Field(..., description="The Groq model that was used")
    
    tokens_used: Optional[int] = Field(
        None, 
        description="Approximate number of tokens used (if available)"
    )
    
    status: str = Field(
        default="success",
        description="Status of the operation"
    )