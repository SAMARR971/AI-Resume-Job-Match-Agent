def normalize_skill(skill: str) -> str:
    """Normalize a skill for reliable comparison."""

    skill = str(skill).strip().lower()

    prefixes = [
        "experience with ",
        "experience in ",
        "knowledge of ",
        "familiarity with ",
        "proficiency in ",
        "strong ",
    ]

    for prefix in prefixes:
        if skill.startswith(prefix):
            skill = skill[len(prefix):]

    suffixes = [
        " programming",
        " concepts",
        " skills",
        " experience",
        " knowledge",
    ]

    for suffix in suffixes:
        if skill.endswith(suffix):
            skill = skill[:-len(suffix)]

    return skill.strip()


def skill_matches(resume_skill: str, job_skill: str) -> bool:
    """
    Check whether a resume item satisfies a job requirement.

    Handles:
    - Exact matches
    - Normalized matches
    - Compound requirements
    - Related skill wording
    """

    resume = normalize_skill(resume_skill)
    job = normalize_skill(job_skill)

    # Exact match
    if resume == job:
        return True

    # Data visualization
    if "data visualization" in job:
        if "data visualization" in resume:
            return True

        if "matplotlib" in resume:
            return True

        if "seaborn" in resume:
            return True

    # Matplotlib
    if "matplotlib" in job:
        if "matplotlib" in resume:
            return True

    # Seaborn
    if "seaborn" in job:
        if "seaborn" in resume:
            return True

    # Machine learning
    if "machine learning" in job:
        if "machine learning" in resume:
            return True

        if "scikit-learn" in resume:
            return True

        if "sklearn" in resume:
            return True

    # Data cleaning / preprocessing
    if "data cleaning" in job or "preprocessing" in job:
        if "data cleaning" in resume:
            return True

        if "cleaning data" in resume:
            return True

        if "preprocessing" in resume:
            return True

        if "data preprocessing" in resume:
            return True

    # Exploratory Data Analysis
    if "exploratory data analysis" in job or "eda" in job:
        if "exploratory data analysis" in resume:
            return True

        if "eda" in resume:
            return True

        if "exploratory analysis" in resume:
            return True

    # SQL / databases
    if "sql" in job:
        if "sql" in resume:
            return True

        if "database" in job and "database" in resume:
            return True

    # Generative AI
    if "generative ai" in job:
        if "generative ai" in resume:
            return True

        if "genai" in resume:
            return True

    # Git / GitHub
    if "git and github" in job:
        if "git" in resume and "github" in resume:
            return True

    if "github" in job:
        if "github" in resume:
            return True

    # Streamlit
    if "streamlit" in job:
        if "streamlit" in resume:
            return True

    # Power BI
    if "power bi" in job:
        if "power bi" in resume:
            return True

    # Tableau
    if "tableau" in job:
        if "tableau" in resume:
            return True

    # General partial matching
    if resume in job or job in resume:
        return True

    return False


def _extract_resume_items(resume_data: dict) -> list:
    """
    Collect searchable information from the resume.

    This allows matching against information found in:
    - technical skills
    - soft skills
    - education
    - experience
    - projects
    - certifications
    """

    searchable_items = []

    sections = [
        "technical_skills",
        "soft_skills",
        "education",
        "experience",
        "projects",
        "certifications",
    ]

    for section in sections:

        items = resume_data.get(section, [])

        if not isinstance(items, list):
            items = [items]

        for item in items:

            if isinstance(item, dict):
                for value in item.values():
                    searchable_items.append(str(value))

            else:
                searchable_items.append(str(item))

    return searchable_items


def match_skills(resume_data: dict, job_data: dict) -> dict:
    """Compare resume information with job requirements."""

    # Search across the entire relevant resume
    resume_items = _extract_resume_items(resume_data)

    required_skills = job_data.get(
        "required_technical_skills",
        []
    )

    preferred_skills = job_data.get(
        "preferred_skills",
        []
    )

    matching_required = []
    missing_required = []

    for required_skill in required_skills:

        matched = any(
            skill_matches(resume_item, required_skill)
            for resume_item in resume_items
        )

        if matched:
            matching_required.append(required_skill)
        else:
            missing_required.append(required_skill)

    matching_preferred = []
    missing_preferred = []

    for preferred_skill in preferred_skills:

        matched = any(
            skill_matches(resume_item, preferred_skill)
            for resume_item in resume_items
        )

        if matched:
            matching_preferred.append(preferred_skill)
        else:
            missing_preferred.append(preferred_skill)

    return {
        "matching_required_skills": matching_required,
        "missing_required_skills": missing_required,
        "matching_preferred_skills": matching_preferred,
        "missing_preferred_skills": missing_preferred
    }