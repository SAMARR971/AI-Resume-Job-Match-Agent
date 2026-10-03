from src.match_report import generate_match_report


# Latest successful scores
overall_score = 84.17
skill_score = 78.57
experience_score = 100.0
education_score = 100.0
project_score = 50.0
keyword_score = 91.67


# Latest skill matching result
match_result = {
    "matching_required_skills": [
        "Python",
        "Pandas",
        "NumPy",
        "SQL",
        "Machine Learning",
        "Matplotlib",
        "Git"
    ],

    "missing_required_skills": [],

    "matching_preferred_skills": [
        "Scikit-learn",
        "Streamlit"
    ],

    "missing_preferred_skills": [
        "Generative AI"
    ]
}


# Latest recommendations
recommendations = {
    "strengths": [
        "Strong match in required skills.",
        "Matches preferred skills.",
        "Your experience appears relevant.",
        "Your education satisfies the requirements.",
        "Your resume contains most important keywords."
    ],

    "areas_to_improve": [
        "Missing preferred skill: Generative AI.",
        "Your projects are partially relevant."
    ],

    "recommendations": [
        "Emphasize the parts of your projects that demonstrate "
        "skills required by the job."
    ]
}


# Generate final report
report = generate_match_report(
    overall_score,
    skill_score,
    experience_score,
    education_score,
    project_score,
    keyword_score,
    match_result,
    recommendations
)


# Display report
print("=" * 60)
print("FINAL RESUME-JOB MATCH REPORT")
print("=" * 60)

print(f"\nOverall Match Score: {report['overall_score']}%")

print("\nSCORE BREAKDOWN:")

for name, score in report["score_breakdown"].items():
    print(f"{name}: {score}%")


print("\nMATCHING REQUIRED SKILLS:")

for skill in report["skills"]["matching_required"]:
    print(f"✓ {skill}")


print("\nMISSING REQUIRED SKILLS:")

for skill in report["skills"]["missing_required"]:
    print(f"✗ {skill}")


print("\nMATCHING PREFERRED SKILLS:")

for skill in report["skills"]["matching_preferred"]:
    print(f"✓ {skill}")


print("\nMISSING PREFERRED SKILLS:")

for skill in report["skills"]["missing_preferred"]:
    print(f"✗ {skill}")


print("\nSTRENGTHS:")

for strength in report["strengths"]:
    print(f"✓ {strength}")


print("\nAREAS TO IMPROVE:")

for area in report["areas_to_improve"]:
    print(f"• {area}")


print("\nRECOMMENDATIONS:")

for recommendation in report["recommendations"]:
    print(f"→ {recommendation}")

print("\n" + "=" * 60)