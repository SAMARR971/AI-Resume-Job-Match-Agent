from src.resume_parser import extract_resume_text
from src.analyzer import analyze_resume
from src.job_analyzer import analyze_job_description
from src.matcher import match_skills


# Resume
resume_text = extract_resume_text("data/test_resume.pdf")
resume_data = analyze_resume(resume_text)


# Job description
with open("data/test_job.txt", "r", encoding="utf-8") as file:
    job_description = file.read()

job_data = analyze_job_description(job_description)


# Match resume against job
match_result = match_skills(resume_data, job_data)


print("=" * 60)
print("SKILL MATCHING RESULT")
print("=" * 60)

print("\nMatching Required Skills:")
print(match_result["matching_required_skills"])

print("\nMissing Required Skills:")
print(match_result["missing_required_skills"])

print("\nMatching Preferred Skills:")
print(match_result["matching_preferred_skills"])

print("\nMissing Preferred Skills:")
print(match_result["missing_preferred_skills"])