from src.agent_llm import create_gemini_agent


agent = create_gemini_agent()


resume_path = "data/test_resume.pdf"

job_description = """
Data Science Intern

We are looking for a Data Science Intern to join our team.

Requirements:
- Currently pursuing a Bachelor's degree in Data Science, Computer Science,
  Statistics, or a related field.
- Strong Python programming skills.
- Experience with Pandas and NumPy.
- Knowledge of SQL.
- Understanding of machine learning concepts.
- Experience with data visualization using Matplotlib or similar tools.
- Familiarity with Git.

Preferred:
- Experience with Scikit-learn.
- Experience building machine learning projects.
- Knowledge of Streamlit.
- Familiarity with Generative AI.

Responsibilities:
- Clean and preprocess datasets.
- Perform exploratory data analysis.
- Build and evaluate machine learning models.
- Create data visualizations.
- Write SQL queries.
- Communicate analytical findings to the team.
"""


response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": f"""
Perform a complete resume-to-job match analysis.

Resume PDF:
{resume_path}

Job Description:
{job_description}

Follow the complete analysis process.

1. Read the resume PDF.
2. Analyze and structure the resume.
3. Analyze and structure the job description.
4. Match the resume against the job requirements.
5. Calculate the skill score.
6. Calculate experience, education, project, and keyword scores.
7. Calculate the overall score.
8. Generate strengths, areas to improve, and recommendations.
9. Generate the final match report.

Use the available tools instead of manually calculating results.

Return the final match report with the scores, matching skills,
missing skills, strengths, areas to improve, and recommendations.
"""
            }
        ]
    }
)


print("=" * 60)
print("END-TO-END RESUME JOB MATCH TEST")
print("=" * 60)

for message in response["messages"]:
    print("\nMESSAGE TYPE:", type(message).__name__)
    print(message)