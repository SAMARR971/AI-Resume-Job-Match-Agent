from src.resume_parser import extract_resume_text
from src.analyzer import analyze_resume
from src.job_analyzer import analyze_job_description

from src.comparison import (
    calculate_experience_score,
    calculate_education_score,
    calculate_project_score,
    calculate_keyword_score
)


# Analyze resume
resume_text = extract_resume_text("data/test_resume.pdf")
resume_data = analyze_resume(resume_text)


# Read job description
with open("data/test_job.txt", "r", encoding="utf-8") as file:
    job_description = file.read()


# Analyze job description
job_data = analyze_job_description(job_description)


# Calculate individual scores
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


# Display results
print("=" * 60)
print("RESUME-JOB COMPARISON")
print("=" * 60)

print(f"\nExperience Score: {experience_score}%")
print(f"Education Score:  {education_score}%")
print(f"Project Score:    {project_score}%")
print(f"Keyword Score:    {keyword_score}%")