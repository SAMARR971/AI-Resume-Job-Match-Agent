from src.recommendations import generate_recommendations


# Use the scores from our latest successful test
skill_match_result = {
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


experience_score = 100.0
education_score = 100.0
project_score = 50.0
keyword_score = 91.67


# Generate recommendations
result = generate_recommendations(
    skill_match_result,
    experience_score,
    education_score,
    project_score,
    keyword_score
)


# Display results
print("=" * 60)
print("RESUME RECOMMENDATIONS")
print("=" * 60)

print("\nSTRENGTHS:")
for strength in result["strengths"]:
    print(f"✓ {strength}")

print("\nAREAS TO IMPROVE:")
for area in result["areas_to_improve"]:
    print(f"• {area}")

print("\nRECOMMENDATIONS:")
for recommendation in result["recommendations"]:
    print(f"→ {recommendation}")