from src.tools import (
    skill_matching_tool,
    skill_scoring_tool,
    comparison_scoring_tool,
    overall_scoring_tool,
    recommendation_tool,
    report_tool
)


resume_data = {
    "technical_skills": [
        "Python",
        "SQL",
        "Pandas",
        "NumPy",
        "Scikit-learn",
        "Matplotlib",
        "Machine Learning",
        "Data Analysis",
        "Data Visualization",
        "Git",
        "Streamlit"
    ],
    "education": [
        {
            "degree": "Bachelor of Science in Data Science",
            "institution": "University Student",
            "dates": "2023–2027"
        }
    ],
    "experience": [
        {
            "title": "Data Science Intern",
            "company": "Tech Solutions",
            "dates": "2025–2026",
            "description": (
                "Assisted with data cleaning, exploratory analysis, "
                "SQL queries, and preparation of analytical reports."
            )
        }
    ],
    "projects": [
        {
            "title": "Customer Churn Prediction",
            "description": (
                "Built a machine learning model using Python and "
                "Scikit-learn to predict customer churn."
            )
        },
        {
            "title": "Sales Data Analysis",
            "description": (
                "Cleaned and analyzed sales data using Pandas "
                "and created visualizations."
            )
        }
    ],
    "certifications": [
        "Introduction to Generative AI",
        "Agentic AI and LangChain Fundamentals"
    ]
}


job_data = {
    "required_technical_skills": [
        "Python",
        "Pandas",
        "NumPy",
        "SQL",
        "Machine Learning",
        "Matplotlib",
        "Git"
    ],
    "required_education": [
        "Bachelor's degree in Data Science, Computer Science, Statistics, or related field"
    ],
    "required_experience": [
        "Pandas/NumPy",
        "data visualization experience"
    ],
    "preferred_skills": [
        "Scikit-learn",
        "Streamlit",
        "Generative AI"
    ],
    "responsibilities": [
        "Clean and preprocess datasets",
        "Perform exploratory data analysis",
        "Build and evaluate machine learning models",
        "Create data visualizations",
        "Write SQL queries",
        "Communicate analytical findings"
    ],
    "important_keywords": [
        "Data Science Intern",
        "Python",
        "Pandas",
        "NumPy",
        "SQL",
        "Machine Learning",
        "Matplotlib",
        "Data Visualization",
        "Git",
        "Scikit-learn",
        "Streamlit",
        "Generative AI"
    ]
}


# Test skill matching
match_result = skill_matching_tool.invoke({
    "resume_data": resume_data,
    "job_data": job_data
})

print("=" * 60)
print("LANGCHAIN TOOL TEST")
print("=" * 60)

print("\nSkill Matching:")
print(match_result)


# Test skill scoring
skill_score = skill_scoring_tool.invoke({
    "match_result": match_result
})

print("\nSkill Score:")
print(skill_score)


# Test comparison scoring
comparison_scores = comparison_scoring_tool.invoke({
    "resume_data": resume_data,
    "job_data": job_data
})

print("\nComparison Scores:")
print(comparison_scores)


# Calculate overall score
overall_score = overall_scoring_tool.invoke({
    "skill_score": skill_score,
    **comparison_scores
})

print("\nOverall Score:")
print(overall_score)


# Test recommendations
recommendations = recommendation_tool.invoke({
    "match_result": match_result,
    **comparison_scores
})

print("\nRecommendations:")
print(recommendations)


print("\n" + "=" * 60)
print("LANGCHAIN TOOLS TEST COMPLETED")
print("=" * 60)