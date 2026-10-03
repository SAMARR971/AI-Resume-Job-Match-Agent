
def _text_from_list(items: list) -> str:
    """Convert strings and dictionaries into searchable lowercase text."""

    text_parts = []

    for item in items:
        if isinstance(item, dict):
            text_parts.append(
                " ".join(str(value) for value in item.values())
            )
        else:
            text_parts.append(str(item))

    return " ".join(text_parts).lower()


def _keyword_match_score(resume_text: str, keywords: list) -> float:
    """Calculate the percentage of keywords found in resume text."""

    if not keywords:
        return 100.0

    matched = 0

    for keyword in keywords:
        if keyword.lower() in resume_text:
            matched += 1

    return round(
        (matched / len(keywords)) * 100,
        2
    )


def _group_match(text: str, alternatives: list) -> bool:
    """
    Return True if any alternative term appears in the text.

    Example:
        ["exploratory data analysis", "exploratory analysis"]
    """

    return any(
        alternative.lower() in text
        for alternative in alternatives
    )


def calculate_experience_score(
    resume_data: dict,
    job_data: dict
) -> float:
    """
    Calculate experience relevance.

    The score considers:
    - Direct evidence in work experience
    - Relevant technical skills
    - Relevant responsibilities

    Direct work experience is weighted more heavily than
    skills alone.
    """

    resume_experience = resume_data.get("experience", [])
    resume_skills = resume_data.get("technical_skills", [])

    required_experience = job_data.get(
        "required_experience",
        []
    )

    responsibilities = job_data.get(
        "responsibilities",
        []
    )

    # If the job gives no experience requirements
    # or responsibilities, do not penalize the candidate.
    if not required_experience and not responsibilities:
        return 100.0

    # If there is no experience at all, give credit only
    # for relevant skills.
    experience_text = _text_from_list(
        resume_experience
    )

    skills_text = _text_from_list(
        resume_skills
    )

    job_text = (
        _text_from_list(required_experience)
        + " "
        + _text_from_list(responsibilities)
    )

    # Each group represents one type of relevant experience.
    experience_groups = [
        [
            "python"
        ],
        [
            "sql",
            "sql quer",
            "database"
        ],
        [
            "pandas"
        ],
        [
            "numpy"
        ],
        [
            "machine learning",
            "machine-learning"
        ],
        [
            "data analysis",
            "data analytics",
            "exploratory analysis",
            "exploratory data analysis"
        ],
        [
            "data cleaning",
            "cleaning data",
            "cleaned data",
            "data preprocessing",
            "preprocessing"
        ],
        [
            "data visualization",
            "data visualisation",
            "visualization",
            "visualisations"
        ],
        [
            "matplotlib"
        ],
        [
            "scikit-learn",
            "sklearn"
        ],
        [
            "model",
            "models",
            "modeling",
            "modelling"
        ],
        [
            "dataset",
            "datasets"
        ],
        [
            "report",
            "reports",
            "analytical report"
        ]
    ]

    # Only use experience categories that are relevant
    # to this particular job.
    relevant_groups = [
        group
        for group in experience_groups
        if _group_match(job_text, group)
    ]

    if not relevant_groups:
        return 100.0

    direct_matches = 0
    skill_matches = 0

    for group in relevant_groups:

        # First check actual work experience.
        if _group_match(experience_text, group):
            direct_matches += 1

        # Then check technical skills.
        elif _group_match(skills_text, group):
            skill_matches += 1

    total = len(relevant_groups)

    # Direct experience receives 80% credit.
    # Skills provide supporting evidence with 50% credit.
    weighted_score = (
        (direct_matches * 1.0)
        + (skill_matches * 0.5)
    ) / total * 100

    return round(
        min(weighted_score, 100.0),
        2
    )


def calculate_education_score(
    resume_data: dict,
    job_data: dict
) -> float:
    """
    Calculate education compatibility.
    """

    resume_education = resume_data.get(
        "education",
        []
    )

    required_education = job_data.get(
        "required_education",
        []
    )

    # No education requirement.
    if not required_education:
        return 100.0

    # Requirement exists but resume has no education.
    if not resume_education:
        return 0.0

    resume_text = _text_from_list(
        resume_education
    )

    required_text = _text_from_list(
        required_education
    )

    # Exact relevant-field matches.
    education_fields = [
        [
            "data science"
        ],
        [
            "computer science"
        ],
        [
            "statistics"
        ],
        [
            "information technology",
            "information systems"
        ],
        [
            "software engineering",
            "software development"
        ]
    ]

    for field_group in education_fields:

        if (
            _group_match(required_text, field_group)
            and _group_match(resume_text, field_group)
        ):
            return 100.0

    # Degree-level matching.
    degree_levels = [
        "bachelor",
        "master",
        "phd"
    ]

    for degree in degree_levels:

        if (
            degree in required_text
            and degree in resume_text
        ):
            return 90.0

    # A related-field requirement with a degree
    # provides partial compatibility.
    if "related field" in required_text:

        if any(
            degree in resume_text
            for degree in degree_levels
        ):
            return 75.0

    return 0.0


def calculate_project_score(
    resume_data: dict,
    job_data: dict
) -> float:
    """
    Calculate project relevance.

    Projects are evaluated against the actual
    responsibilities of the job.
    """

    projects = resume_data.get(
        "projects",
        []
    )

    responsibilities = job_data.get(
        "responsibilities",
        []
    )

    # If the job has no project-related responsibilities,
    # do not penalize the candidate.
    if not responsibilities:
        return 100.0

    # If the candidate has no projects.
    if not projects:
        return 0.0

    project_text = _text_from_list(
        projects
    )

    job_text = _text_from_list(
        responsibilities
    )

    # Groups represent concepts rather than exact phrases.
    project_groups = [
        [
            "data cleaning",
            "cleaned data",
            "clean data",
            "preprocess",
            "preprocessing"
        ],
        [
            "data analysis",
            "data analytics",
            "analyze data",
            "analysed data",
            "analyzed data",
            "exploratory analysis",
            "exploratory data analysis"
        ],
        [
            "machine learning",
            "machine-learning"
        ],
        [
            "model",
            "models",
            "modeling",
            "modelling",
            "predict"
        ],
        [
            "evaluate model",
            "evaluated model",
            "model evaluation",
            "model performance",
            "evaluate"
        ],
        [
            "data visualization",
            "data visualisation",
            "visualization",
            "visualisations",
            "visualize",
            "visualise"
        ],
        [
            "python"
        ],
        [
            "sql",
            "sql quer"
        ],
        [
            "pandas"
        ],
        [
            "numpy"
        ]
    ]

    # Find concepts actually relevant to the job.
    relevant_groups = [
        group
        for group in project_groups
        if _group_match(job_text, group)
    ]

    if not relevant_groups:
        return 100.0

    matched_groups = 0

    for group in relevant_groups:

        if _group_match(project_text, group):
            matched_groups += 1

    score = (
        matched_groups
        / len(relevant_groups)
    ) * 100

    return round(
        score,
        2
    )


def calculate_keyword_score(
    resume_data: dict,
    job_data: dict
) -> float:
    """
    Calculate important keyword coverage.

    This checks the complete structured resume,
    including skills, education, experience,
    projects, and certifications.
    """

    resume_text = _text_from_list(
        list(resume_data.values())
    )

    keywords = job_data.get(
        "important_keywords",
        []
    )

    if not keywords:
        return 100.0

    return _keyword_match_score(
        resume_text,
        keywords
    )

