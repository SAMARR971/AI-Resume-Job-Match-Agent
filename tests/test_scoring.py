from src.resume_parser import extract_resume_text
from src.analyzer import analyze_resume
from src.job_analyzer import analyze_job_description
from src.matcher import match_skills
from src.scoring import calculate_skill_score


# Analyze resume
resume_text = extract_resume_text("data/test_resume.pdf")
resume_data = analyze_resume(resume_text)


# Analyze job description
with open("data/test_job.txt", "r", encoding="utf-8") as file:
    job_description = file.read()

job_data = analyze_job_description(job_description)


# Match skills
match_result = match_skills(resume_data, job_data)


# Calculate score
score = calculate_skill_score(match_result)


print("=" * 60)
print("RESUME-JOB MATCH SCORE")
print("=" * 60)

print(f"\nSkill Match Score: {score}%")

print("\nMatching Required Skills:")
print(match_result["matching_required_skills"])

print("\nMissing Required Skills:")
print(match_result["missing_required_skills"])

print("\nMatching Preferred Skills:")
print(match_result["matching_preferred_skills"])

print("\nMissing Preferred Skills:")
print(match_result["missing_preferred_skills"])