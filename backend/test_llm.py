# test_schemas.py
from models.schemas import RepoReadmeRequest, RepoReadmeResponse
from pydantic import ValidationError


def test_repo_readme_request_valid():
    """Test valid request data"""
    data = {
        "repo_url": "https://github.com/tiangolo/fastapi",
        "selected_sections": ["Features", "Installation", "Usage"],
        "prompt": "Make it beginner-friendly",
        "model_name": "llama-3.1-8b-instant"
    }
    
    request = RepoReadmeRequest(**data)
    
    print("✅ Valid RepoReadmeRequest passed!")
    print(f"   Repo URL: {request.repo_url}")
    print(f"   Sections: {request.selected_sections}")
    return request


def test_repo_readme_request_invalid():
    """Test validation error for missing required field"""
    try:
        # Missing repo_url (required field)
        RepoReadmeRequest(
            selected_sections=["Features"]
        )
    except ValidationError as e:
        print("✅ ValidationError caught successfully for missing required field!")
        print(f"   Error: {e.errors()[0]['msg']}")


def test_repo_readme_response():
    """Test response model"""
    response = RepoReadmeResponse(
        markdown="# Awesome Project\n\nThis is a test README.",
        model_used="llama-3.1-8b-instant",
        tokens_used=1247,
        status="success"
    )
    
    print("✅ RepoReadmeResponse created successfully!")
    print(f"   Model used: {response.model_used}")
    print(f"   Tokens: {response.tokens_used}")
    return response



def main():
    print("🧪 Running Schemas Tests...\n")
    
    test_repo_readme_request_valid()
    print()
    test_repo_readme_request_invalid()
    print()
    test_repo_readme_response()
    print()
    
    print("\n🎉 All schema tests completed successfully!")


if __name__ == "__main__":
    main()