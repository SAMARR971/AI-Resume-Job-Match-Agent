import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()


def analyze_job_description(job_description: str) -> dict:
    """Analyze a job description using Gemini and return structured data."""

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env")

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are an expert job description analyzer.

Analyze the job description below.

IMPORTANT:
- Use ONLY information explicitly present in the job description.
- Do not invent requirements or qualifications.
- Return ONLY valid JSON.
- Do not include markdown or ```.

Use exactly this JSON structure:

{{
    "job_title": "",
    "required_technical_skills": [],
    "required_soft_skills": [],
    "required_education": [],
    "required_experience": [],
    "preferred_skills": [],
    "responsibilities": [],
    "important_keywords": []
}}

JOB DESCRIPTION:
-------------------------
{job_description}
-------------------------
"""

    response = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt
    )

    result = response.output_text

    return json.loads(result)