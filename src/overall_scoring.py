def calculate_overall_score(
    skill_score: float,
    experience_score: float,
    education_score: float,
    project_score: float,
    keyword_score: float
) -> float:
    """
    Calculate the overall resume-job match score.

    Weights:
    Skills       = 35%
    Experience   = 25%
    Education    = 15%
    Projects     = 15%
    Keywords     = 10%
    """

    overall_score = (
        skill_score * 0.35
        + experience_score * 0.25
        + education_score * 0.15
        + project_score * 0.15
        + keyword_score * 0.10
    )

    return round(overall_score, 2)