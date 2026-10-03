def generate_match_report(
    overall_score: float,
    skill_score: float,
    experience_score: float,
    education_score: float,
    project_score: float,
    keyword_score: float,
    match_result: dict,
    recommendations: dict
) -> dict:
    """Create a complete resume-job match report."""

    return {
        "overall_score": overall_score,

        "score_breakdown": {
            "skill_score": skill_score,
            "experience_score": experience_score,
            "education_score": education_score,
            "project_score": project_score,
            "keyword_score": keyword_score
        },

        "skills": {
            "matching_required": match_result.get(
                "matching_required_skills", []
            ),
            "missing_required": match_result.get(
                "missing_required_skills", []
            ),
            "matching_preferred": match_result.get(
                "matching_preferred_skills", []
            ),
            "missing_preferred": match_result.get(
                "missing_preferred_skills", []
            )
        },

        "strengths": recommendations.get(
            "strengths", []
        ),

        "areas_to_improve": recommendations.get(
            "areas_to_improve", []
        ),

        "recommendations": recommendations.get(
            "recommendations", []
        )
    }