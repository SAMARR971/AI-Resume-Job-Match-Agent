import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()


def analyze_resume(resume_text: str) -> dict:
    """Analyze resume text using Gemini and return structured data."""

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env")

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are an expert resume analyzer.

Analyze the resume below.

IMPORTANT:
- Use ONLY information explicitly present in the resume.
- Do not invent skills, experience, education, certifications, projects,
  or achievements.
- Return ONLY valid JSON.
- Do not include markdown or ```.

Use exactly this JSON structure:

{{
    "candidate_name": "",
    "summary": "",
    "technical_skills": [],
    "soft_skills": [],
    "education": [],
    "experience": [],
    "projects": [],
    "certifications": []
}}

RESUME:
-------------------------
{resume_text}
-------------------------
"""

    response = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt
    )

    result = response.output_text

    return json.loads(result)