from typing import List, Optional

def build_readme_prompt(
        repo_context: str,
        selected_sections: Optional[List[str]] = None,
        custom_instructions: Optional[List[str]] = None,
        project_purpose: Optional[List[str]] = None
) -> str:
    """
    Builds a high-quality, well-engineered prompt for generating a README.
    
    Args:
        repo_context (str): Full context from repo_parser (structure + key files)
        selected_sections (List[str]): Sections user wants (e.g. Features, Installation...)
        custom_instructions (str): Any extra user instructions
        project_purpose (str): Optional short description of what the project does
    """


    if selected_sections is None:
        selected_sections = [
            "Project Title & Tagline",
            "Description",
            "Features",
            "Tech Stack",
            "Installation",
            "Usage",
            "API Reference (if applicable)",
            "Contributing",
            "License"
        ]

    sections_str = "\n".join([f"- {section}" for section in selected_sections])

    prompt = f"""You are an expert technical writer and README specialist.

            Generate a **professional, modern, and engaging** README.md for the following project.

            ### Project Context:
            {repo_context}

            ### Desired Sections:
            {sections_str}

            ### Additional Guidelines:
            - Use clear, developer-friendly language.
            - Make it visually appealing with proper Markdown (badges, code blocks, tables, emojis where appropriate).
            - Be concise but informative.
            - Highlight what makes this project unique.

            ### Rules:
            - Never reproduce the full license text, only state the license name and year
            - Do not use filler phrases like "innovative", "robust", "seamless"
            - If the repo URL is unknown, do not guess it — write [your-repo-url] as placeholder
            - Keep descriptions specific to what the code actually does
            - Do not invent features that are not found in the code
            """
    
    if project_purpose:
        prompt += f"\n### Project Purpose:\n{project_purpose}\n"

    if custom_instructions:
        prompt += f"\n### Custom Instructions:\n{custom_instructions}\n"

    prompt += """
    Return only the complete README.md content. Do not include any explanations, comments, or markdown code blocks (```) around the output.
    Start directly with the README content.
    """

    return prompt.strip()