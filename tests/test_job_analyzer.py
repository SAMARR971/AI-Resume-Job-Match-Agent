from src.job_analyzer import analyze_job_description


job_file = "data/test_job.txt"

with open(job_file, "r", encoding="utf-8") as file:
    job_description = file.read()


analysis = analyze_job_description(job_description)


print("=" * 60)
print("STRUCTURED JOB DESCRIPTION ANALYSIS")
print("=" * 60)

for key, value in analysis.items():
    print(f"\n{key}:")
    print(value)