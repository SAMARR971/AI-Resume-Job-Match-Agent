from langchain.tools import tool

from src.resume_parser import extract_resume_text
from src.analyzer import analyze_resume
from src.job_analyzer import analyze_job_description
from src.matcher import match_skills
from src.scoring import calculate_skill_score

from src.comparison import (
    calculate_experience_score,
    calculate_education_score,
    calculate_project_score,
    calculate_keyword_score
)

from src.overall_scoring import calculate_overall_score

from src.recommendations import generate_recommendations

from src.match_report import generate_match_report


@tool
def resume_parser_tool(pdf_path: str) -> str:
    """Extract text from a resume PDF."""

    return extract_resume_text(pdf_path)


@tool
def resume_analysis_tool(resume_text: str) -> dict:
    """Analyze resume text using Gemini."""

    return analyze_resume(resume_text)


@tool
def job_analysis_tool(job_description: str) -> dict:
    """Analyze a job description using Gemini."""

    return analyze_job_description(job_description)


@tool
def skill_matching_tool(
    resume_data: dict,
    job_data: dict
) -> dict:
    """Match resume skills against job requirements."""

    return match_skills(
        resume_data,
        job_data
    )


@tool
def skill_scoring_tool(match_result: dict) -> float:
    """Calculate the skill match score."""

    return calculate_skill_score(
        match_result
    )


@tool
def comparison_scoring_tool(
    resume_data: dict,
    job_data: dict
) -> dict:
    """Calculate experience, education, project, and keyword scores."""

    experience_score = calculate_experience_score(
        resume_data,
        job_data
    )

    education_score = calculate_education_score(
        resume_data,
        job_data
    )

    project_score = calculate_project_score(
        resume_data,
        job_data
    )

    keyword_score = calculate_keyword_score(
        resume_data,
        job_data
    )

    return {
        "experience_score": experience_score,
        "education_score": education_score,
        "project_score": project_score,
        "keyword_score": keyword_score
    }


@tool
def overall_scoring_tool(
    skill_score: float,
    experience_score: float,
    education_score: float,
    project_score: float,
    keyword_score: float
) -> float:
    """Calculate the overall resume-job match score."""

    return calculate_overall_score(
        skill_score,
        experience_score,
        education_score,
        project_score,
        keyword_score
    )


@tool
def recommendation_tool(
    match_result: dict,
    experience_score: float,
    education_score: float,
    project_score: float,
    keyword_score: float
) -> dict:
    """Generate personalized resume recommendations."""

    return generate_recommendations(
        match_result,
        experience_score,
        education_score,
        project_score,
        keyword_score
    )


@tool
def report_tool(
    overall_score: float,
    skill_score: float,
    experience_score: float,
    education_score: float,
    project_score: float,
    keyword_score: float,
    match_result: dict,
    recommendations: dict
) -> dict:
    """Generate the final resume-job match report."""

    return generate_match_report(
        overall_score,
        skill_score,
        experience_score,
        education_score,
        project_score,
        keyword_score,
        match_result,
        recommendations
    )


# All available tools
TOOLS = [
    resume_parser_tool,
    resume_analysis_tool,
    job_analysis_tool,
    skill_matching_tool,
    skill_scoring_tool,
    comparison_scoring_tool,
    overall_scoring_tool,
    recommendation_tool,
    report_tool
]