def calculate_skill_score(match_result: dict) -> float:
    """Calculate a skill match score."""

    matching_required = match_result.get("matching_required_skills", [])
    missing_required = match_result.get("missing_required_skills", [])

    matching_preferred = match_result.get("matching_preferred_skills", [])
    missing_preferred = match_result.get("missing_preferred_skills", [])

    # Required skills score
    total_required = len(matching_required) + len(missing_required)

    if total_required > 0:
        required_score = (
            len(matching_required) / total_required
        ) * 100
    else:
        required_score = 0

    # Preferred skills score
    total_preferred = len(matching_preferred) + len(missing_preferred)

    if total_preferred > 0:
        preferred_score = (
            len(matching_preferred) / total_preferred
        ) * 100
    else:
        preferred_score = 0

    # Required skills are more important
    if total_required > 0 and total_preferred > 0:
        final_score = (
            required_score * 0.8
            + preferred_score * 0.2
        )
    elif total_required > 0:
        final_score = required_score
    else:
        final_score = preferred_score

    return round(final_score, 2)