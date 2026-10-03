def generate_recommendations(
    match_result: dict,
    experience_score: float,
    education_score: float,
    project_score: float,
    keyword_score: float
) -> dict:
    """Generate resume improvement recommendations."""

    recommendations = []
    strengths = []
    areas_to_improve = []

    # -------------------------
    # Skill Analysis
    # -------------------------

    matching_required = match_result.get(
        "matching_required_skills", []
    )

    missing_required = match_result.get(
        "missing_required_skills", []
    )

    matching_preferred = match_result.get(
        "matching_preferred_skills", []
    )

    missing_preferred = match_result.get(
        "missing_preferred_skills", []
    )

    # Strengths
    if matching_required:
        strengths.append(
            f"Strong match in required skills: "
            f"{', '.join(matching_required)}."
        )

    if matching_preferred:
        strengths.append(
            f"Matches preferred skills: "
            f"{', '.join(matching_preferred)}."
        )

    # Missing skills
    if missing_required:
        areas_to_improve.append(
            f"Missing required skills: "
            f"{', '.join(missing_required)}."
        )

        recommendations.append(
            "Consider gaining experience with the missing required "
            "skills before applying, if they are genuinely required "
            "for the position."
        )

    if missing_preferred:
        areas_to_improve.append(
            f"Missing preferred skills: "
            f"{', '.join(missing_preferred)}."
        )

    # -------------------------
    # Experience
    # -------------------------

    if experience_score >= 80:
        strengths.append(
            "Your experience appears relevant to the job requirements."
        )
    elif experience_score >= 50:
        areas_to_improve.append(
            "Your experience has some relevance but could be "
            "better aligned with the job requirements."
        )
        recommendations.append(
            "Highlight the experience that most closely matches "
            "the responsibilities in the job description."
        )
    else:
        areas_to_improve.append(
            "Your experience has limited overlap with the job requirements."
        )
        recommendations.append(
            "Build or highlight more experience related to the "
            "main responsibilities of this position."
        )

    # -------------------------
    # Education
    # -------------------------

    if education_score >= 80:
        strengths.append(
            "Your education appears to satisfy the job's education requirements."
        )
    else:
        areas_to_improve.append(
            "Your education does not fully match the stated requirements."
        )

    # -------------------------
    # Projects
    # -------------------------

    if project_score >= 80:
        strengths.append(
            "Your projects demonstrate strong relevance to the position."
        )
    elif project_score >= 50:
        areas_to_improve.append(
            "Your projects are partially relevant to the position."
        )
        recommendations.append(
            "Emphasize the parts of your projects that demonstrate "
            "skills required by the job."
        )
    else:
        areas_to_improve.append(
            "Your projects have limited relevance to the position."
        )
        recommendations.append(
            "Consider building projects that directly demonstrate "
            "the skills and responsibilities required by the job."
        )

    # -------------------------
    # Keywords
    # -------------------------

    if keyword_score >= 80:
        strengths.append(
            "Your resume contains most of the important keywords "
            "from the job description."
        )
    else:
        areas_to_improve.append(
            "Your resume is missing several important job keywords."
        )
        recommendations.append(
            "Use relevant keywords from the job description when "
            "they accurately describe your existing skills and experience."
        )

    # -------------------------
    # Return Results
    # -------------------------

    return {
        "strengths": strengths,
        "areas_to_improve": areas_to_improve,
        "recommendations": recommendations
    }