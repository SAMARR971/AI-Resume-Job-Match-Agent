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


# -------------------------
# Analyze Resume
# -------------------------

resume_text = extract_resume_text("data/test_resume.pdf")
resume_data = analyze_resume(resume_text)


# -------------------------
# Analyze Job Description
# -------------------------

with open("data/test_job.txt", "r", encoding="utf-8") as file:
    job_description = file.read()

job_data = analyze_job_description(job_description)


# -------------------------
# Skill Matching
# -------------------------

match_result = match_skills(resume_data, job_data)


# -------------------------
# Calculate Skill Score
# -------------------------

skill_score = calculate_skill_score(match_result)


# -------------------------
# Calculate Other Scores
# -------------------------

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


# -------------------------
# Calculate Overall Score
# -------------------------

overall_score = calculate_overall_score(
    skill_score,
    experience_score,
    education_score,
    project_score,
    keyword_score
)


# -------------------------
# Display Results
# -------------------------

print("=" * 60)
print("FINAL RESUME-JOB MATCH SCORE")
print("=" * 60)

print(f"\nSkill Score:       {skill_score}%")
print(f"Experience Score:  {experience_score}%")
print(f"Education Score:   {education_score}%")
print(f"Project Score:     {project_score}%")
print(f"Keyword Score:     {keyword_score}%")

print("\n" + "-" * 60)

print(f"OVERALL MATCH SCORE: {overall_score}%")

print("=" * 60)