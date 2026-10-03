from typing import TypedDict

from langgraph.graph import StateGraph, START, END

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


class AgentState(TypedDict, total=False):
    resume_path: str
    job_description: str

    resume_text: str
    resume_data: dict
    job_data: dict

    match_result: dict

    skill_score: float
    experience_score: float
    education_score: float
    project_score: float
    keyword_score: float

    overall_score: float

    recommendations: dict
    final_report: dict


def analyze_resume_node(state: AgentState):
    """Extract and analyze the resume."""

    print("1. Analyzing resume...")

    resume_text = extract_resume_text(
        state["resume_path"]
    )

    resume_data = analyze_resume(
        resume_text
    )

    return {
        "resume_text": resume_text,
        "resume_data": resume_data
    }


def analyze_job_node(state: AgentState):
    """Analyze the job description."""

    print("2. Analyzing job description...")

    job_data = analyze_job_description(
        state["job_description"]
    )

    return {
        "job_data": job_data
    }


def match_skills_node(state: AgentState):
    """Match resume skills against job requirements."""

    print("3. Matching skills...")

    match_result = match_skills(
        state["resume_data"],
        state["job_data"]
    )

    skill_score = calculate_skill_score(
        match_result
    )

    return {
        "match_result": match_result,
        "skill_score": skill_score
    }


def calculate_score_node(state: AgentState):
    """Calculate all comparison scores."""

    print("4. Calculating scores...")

    experience_score = calculate_experience_score(
        state["resume_data"],
        state["job_data"]
    )

    education_score = calculate_education_score(
        state["resume_data"],
        state["job_data"]
    )

    project_score = calculate_project_score(
        state["resume_data"],
        state["job_data"]
    )

    keyword_score = calculate_keyword_score(
        state["resume_data"],
        state["job_data"]
    )

    overall_score = calculate_overall_score(
        state["skill_score"],
        experience_score,
        education_score,
        project_score,
        keyword_score
    )

    return {
        "experience_score": experience_score,
        "education_score": education_score,
        "project_score": project_score,
        "keyword_score": keyword_score,
        "overall_score": overall_score
    }


def recommendations_node(state: AgentState):
    """Generate recommendations."""

    print("5. Generating recommendations...")

    recommendations = generate_recommendations(
        state["match_result"],
        state["experience_score"],
        state["education_score"],
        state["project_score"],
        state["keyword_score"]
    )

    return {
        "recommendations": recommendations
    }


def final_report_node(state: AgentState):
    """Create the final match report."""

    print("6. Creating final report...")

    final_report = generate_match_report(
        state["overall_score"],
        state["skill_score"],
        state["experience_score"],
        state["education_score"],
        state["project_score"],
        state["keyword_score"],
        state["match_result"],
        state["recommendations"]
    )

    return {
        "final_report": final_report
    }


# --------------------------------
# Create LangGraph
# --------------------------------

graph = StateGraph(AgentState)


graph.add_node(
    "analyze_resume",
    analyze_resume_node
)

graph.add_node(
    "analyze_job",
    analyze_job_node
)

graph.add_node(
    "match_skills",
    match_skills_node
)

graph.add_node(
    "calculate_score",
    calculate_score_node
)

graph.add_node(
    "recommendations",
    recommendations_node
)

graph.add_node(
    "final_report",
    final_report_node
)


# --------------------------------
# Define Workflow
# --------------------------------

graph.add_edge(
    START,
    "analyze_resume"
)

graph.add_edge(
    "analyze_resume",
    "analyze_job"
)

graph.add_edge(
    "analyze_job",
    "match_skills"
)

graph.add_edge(
    "match_skills",
    "calculate_score"
)

graph.add_edge(
    "calculate_score",
    "recommendations"
)

graph.add_edge(
    "recommendations",
    "final_report"
)

graph.add_edge(
    "final_report",
    END
)


# Compile
app = graph.compile()