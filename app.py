import os
import re
import tempfile

import streamlit as st
from dotenv import load_dotenv

from src.agent_llm import create_gemini_agent


load_dotenv()


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Resume & Job Match Agent",
    page_icon="📄",
    layout="wide"
)


# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------

def extract_final_message(result):
    """Extract the final text message from the agent result."""

    if not result:
        return ""

    messages = result.get("messages", [])

    for message in reversed(messages):

        if hasattr(message, "content"):
            content = message.content

            if isinstance(content, str):
                return content

            if isinstance(content, list):

                text_parts = []

                for item in content:

                    if isinstance(item, dict):
                        if "text" in item:
                            text_parts.append(str(item["text"]))

                    else:
                        text_parts.append(str(item))

                if text_parts:
                    return "\n".join(text_parts)

    return str(result)


def clean_report_text(text):
    """Remove unnecessary markdown formatting for display/PDF."""

    text = text.replace("**", "")
    text = text.replace("### ", "")
    text = text.replace("#### ", "")

    return text.strip()


def extract_overall_score(text):
    """Extract the overall score from the final report."""

    patterns = [
        r"Overall Match Score\s*:?\s*\**\s*(\d+(?:\.\d+)?)\s*%",
        r"Overall Match Score\s*:?\s*\**\s*(\d+(?:\.\d+)?)\s*/\s*100",
        r"Overall Match Score:\s*\**\s*(\d+(?:\.\d+)?)\s*%"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            try:
                score = float(match.group(1))

                if 0 <= score <= 100:
                    return score

            except ValueError:
                pass

    return None


def extract_score(text, score_name):
    """Extract an individual score."""

    score_aliases = {

        "Skill Score": [
            "Skill Match Score",
            "Skill Score"
        ],

        "Experience Score": [
            "Experience Match Score",
            "Experience Score"
        ],

        "Education Score": [
            "Education Match Score",
            "Education Score"
        ],

        "Project Score": [
            "Project Match Score",
            "Project Score"
        ],

        "Keyword Score": [
            "Keyword Match Score",
            "Keyword Score"
        ]
    }

    aliases = score_aliases.get(
        score_name,
        [score_name]
    )

    for alias in aliases:

        percentage_pattern = (
            rf"{re.escape(alias)}"
            rf"\s*:?\s*"
            rf"\*{{0,2}}\s*"
            rf"(\d+(?:\.\d+)?)"
            rf"\s*%"
            rf"\s*\*{{0,2}}"
        )

        match = re.search(
            percentage_pattern,
            text,
            re.IGNORECASE
        )

        if match:

            try:
                score = float(match.group(1))

                if 0 <= score <= 100:
                    return score

            except ValueError:
                pass

        out_of_100_pattern = (
            rf"{re.escape(alias)}"
            rf"\s*:?\s*"
            rf"\*{{0,2}}\s*"
            rf"(\d+(?:\.\d+)?)"
            rf"\s*/\s*100"
            rf"\s*\*{{0,2}}"
        )

        match = re.search(
            out_of_100_pattern,
            text,
            re.IGNORECASE
        )

        if match:

            try:
                score = float(match.group(1))

                if 0 <= score <= 100:
                    return score

            except ValueError:
                pass

    return None


def clean_extracted_items(items):
    """Clean extracted list items."""

    cleaned = []

    for item in items:

        item = item.strip()

        item = re.sub(
            r"^[\-\*\d\.\)\s]+",
            "",
            item
        )

        if item:
            cleaned.append(item)

    return cleaned


def extract_section(text, section_name):
    """Extract bullet/list items from a report section."""

    pattern = (
        rf"(?:###|####)?\s*"
        rf"\**{re.escape(section_name)}\**"
        rf"\s*:?\s*\n"
        rf"(.*?)(?=\n(?:###|####)\s|\Z)"
    )

    match = re.search(
        pattern,
        text,
        re.IGNORECASE | re.DOTALL
    )

    if not match:
        return []

    section_text = match.group(1)

    lines = section_text.splitlines()

    items = []

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if line.startswith("-"):
            items.append(line)

        elif re.match(r"^\d+\.", line):
            items.append(line)

    return clean_extracted_items(items)


def create_pdf(report_text):
    """Create a PDF report and return its bytes."""

    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.enums import TA_CENTER
    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Spacer
    )
    from reportlab.lib.units import inch

    from io import BytesIO

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.6 * inch,
        leftMargin=0.6 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.6 * inch
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER

    heading_style = styles["Heading2"]
    body_style = styles["BodyText"]

    story = []

    story.append(
        Paragraph(
            "AI Resume & Job Match Report",
            title_style
        )
    )

    story.append(
        Spacer(1, 20)
    )

    # Convert report into readable PDF paragraphs.

    lines = report_text.splitlines()

    for line in lines:

        line = line.strip()

        if not line:
            story.append(
                Spacer(1, 8)
            )
            continue

        # Remove markdown.

        line = line.replace("**", "")

        if line.startswith("# "):
            story.append(
                Paragraph(
                    line[2:],
                    title_style
                )
            )

        elif line.startswith("### "):
            story.append(
                Paragraph(
                    line[4:],
                    heading_style
                )
            )

        elif line.startswith("#### "):
            story.append(
                Paragraph(
                    line[5:],
                    heading_style
                )
            )

        elif re.match(r"^\d+\.\s", line):

            story.append(
                Paragraph(
                    line,
                    body_style
                )
            )

        elif line.startswith("- "):

            story.append(
                Paragraph(
                    "• " + line[2:],
                    body_style
                )
            )

        else:

            story.append(
                Paragraph(
                    line,
                    body_style
                )
            )

        story.append(
            Spacer(1, 5)
        )

    document.build(story)

    buffer.seek(0)

    return buffer.getvalue()


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("📄 AI Resume & Job Match Agent")

st.write(
    "Analyze a resume against a job description using "
    "Gemini, LangChain, LangGraph, and deterministic scoring."
)


# ---------------------------------------------------------
# INPUT SECTION
# ---------------------------------------------------------

st.header("📥 Input")

uploaded_resume = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste Job Description",
    height=250,
    placeholder="Paste the complete job description here..."
)


# ---------------------------------------------------------
# ANALYZE BUTTON
# ---------------------------------------------------------

analyze_button = st.button(
    "🚀 Analyze Resume",
    type="primary"
)


if analyze_button:

    if uploaded_resume is None:

        st.error(
            "Please upload a resume PDF."
        )

    elif not job_description.strip():

        st.error(
            "Please enter a job description."
        )

    else:

        temp_pdf_path = None

        try:

            with st.spinner(
                "Analyzing resume and job description..."
            ):

                # Create temporary PDF file.

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".pdf"
                ) as temp_file:

                    temp_file.write(
                        uploaded_resume.getbuffer()
                    )

                    temp_pdf_path = temp_file.name

                # Create Gemini + LangChain agent.

                agent = create_gemini_agent()

                # Invoke the agent.

                result = agent.invoke(
                    {
                        "messages": [
                            {
                                "role": "user",
                                "content": f"""
Analyze this resume against the following job description.

Resume PDF path:
{temp_pdf_path}

Job Description:
{job_description}

Use the resume_parser_tool first to extract the resume text.

Then use the required analysis, matching,
scoring, recommendation, and report tools.

Return the complete final resume-to-job match report.
"""
                            }
                        ]
                    }
                )

                final_report = extract_final_message(
                    result
                )

            if not final_report:

                st.error(
                    "The agent did not return a report."
                )

            else:

                # -------------------------------------------------
                # EXTRACT SCORES
                # -------------------------------------------------

                overall_score = extract_overall_score(
                    final_report
                )

                skill_score = extract_score(
                    final_report,
                    "Skill Score"
                )

                experience_score = extract_score(
                    final_report,
                    "Experience Score"
                )

                education_score = extract_score(
                    final_report,
                    "Education Score"
                )

                project_score = extract_score(
                    final_report,
                    "Project Score"
                )

                keyword_score = extract_score(
                    final_report,
                    "Keyword Score"
                )

                # -------------------------------------------------
                # SAVE REPORT IN SESSION
                # -------------------------------------------------

                st.session_state["final_report"] = final_report

                st.session_state["overall_score"] = overall_score

                st.session_state["skill_score"] = skill_score
                st.session_state["experience_score"] = experience_score
                st.session_state["education_score"] = education_score
                st.session_state["project_score"] = project_score
                st.session_state["keyword_score"] = keyword_score


        except Exception as e:

            st.error(
                f"An error occurred: {e}"
            )

        finally:

            if temp_pdf_path and os.path.exists(
                temp_pdf_path
            ):

                os.remove(
                    temp_pdf_path
                )


# ---------------------------------------------------------
# DISPLAY RESULTS
# ---------------------------------------------------------

if "final_report" in st.session_state:

    final_report = st.session_state[
        "final_report"
    ]

    overall_score = st.session_state.get(
        "overall_score"
    )

    skill_score = st.session_state.get(
        "skill_score"
    )

    experience_score = st.session_state.get(
        "experience_score"
    )

    education_score = st.session_state.get(
        "education_score"
    )

    project_score = st.session_state.get(
        "project_score"
    )

    keyword_score = st.session_state.get(
        "keyword_score"
    )

    # ---------------------------------------------------------
    # MATCH RESULTS
    # ---------------------------------------------------------

    st.header("📊 Match Results")

    if overall_score is not None:

        st.metric(
            "Overall Match Score",
            f"{overall_score:.2f} / 100"
        )

    else:

        st.metric(
            "Overall Match Score",
            "N/A"
        )

    # ---------------------------------------------------------
    # SCORE BREAKDOWN
    # ---------------------------------------------------------

    st.subheader("📈 Score Breakdown")

    col1, col2, col3, col4, col5 = st.columns(5)

    score_data = [
        ("Skills", skill_score),
        ("Experience", experience_score),
        ("Education", education_score),
        ("Projects", project_score),
        ("Keywords", keyword_score)
    ]

    columns = [
        col1,
        col2,
        col3,
        col4,
        col5
    ]

    for column, (label, score) in zip(
        columns,
        score_data
    ):

        with column:

            if score is not None:

                st.metric(
                    label,
                    f"{score:.2f}%"
                )

                st.progress(
                    min(
                        max(
                            score / 100,
                            0.0
                        ),
                        1.0
                    )
                )

            else:

                st.metric(
                    label,
                    "N/A"
                )

    # ---------------------------------------------------------
    # SCORE CHART
    # ---------------------------------------------------------

    st.subheader("📊 Score Visualization")

    chart_data = {
        "Category": [],
        "Score": []
    }

    for label, score in score_data:

        if score is not None:

            chart_data["Category"].append(
                label
            )

            chart_data["Score"].append(
                score
            )

    if chart_data["Category"]:

        import pandas as pd

        chart_df = pd.DataFrame(
            {
                "Score": chart_data["Score"]
            },
            index=chart_data["Category"]
        )

        st.bar_chart(
            chart_df,
            y="Score"
        )

    # ---------------------------------------------------------
    # SKILLS MATCHING
    # ---------------------------------------------------------

    st.header("🧠 Skills Matching")

    matching_required = extract_section(
        final_report,
        "Matching Required Skills"
    )

    missing_required = extract_section(
        final_report,
        "Missing Required Skills"
    )

    matching_preferred = extract_section(
        final_report,
        "Matching Preferred Skills"
    )

    missing_preferred = extract_section(
        final_report,
        "Missing Preferred Skills"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(
            "✅ Matching Required Skills"
        )

        if matching_required:

            for item in matching_required:
                st.success(item)

        else:

            st.info(
                "No matching required skills found."
            )

    with col2:

        st.subheader(
            "❌ Missing Required Skills"
        )

        if missing_required:

            for item in missing_required:
                st.error(item)

        else:

            st.success(
                "No missing required skills."
            )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(
            "⭐ Matching Preferred Skills"
        )

        if matching_preferred:

            for item in matching_preferred:
                st.info(item)

        else:

            st.info(
                "No matching preferred skills found."
            )

    with col2:

        st.subheader(
            "⚠️ Missing Preferred Skills"
        )

        if missing_preferred:

            for item in missing_preferred:
                st.warning(item)

        else:

            st.success(
                "No missing preferred skills."
            )

    # ---------------------------------------------------------
    # STRENGTHS
    # ---------------------------------------------------------

    st.header("💪 Strengths")

    strengths = extract_section(
        final_report,
        "Strengths"
    )

    if strengths:

        for item in strengths:
            st.success(item)

    else:

        st.info(
            "No strengths extracted."
        )

    # ---------------------------------------------------------
    # AREAS TO IMPROVE
    # ---------------------------------------------------------

    st.header("📌 Areas to Improve")

    areas = extract_section(
        final_report,
        "Areas to Improve"
    )

    if areas:

        for item in areas:
            st.warning(item)

    else:

        st.info(
            "No improvement areas extracted."
        )

    # ---------------------------------------------------------
    # RECOMMENDATIONS
    # ---------------------------------------------------------

    st.header("💡 Recommendations")

    recommendations = extract_section(
        final_report,
        "Recommendations"
    )

    if recommendations:

        for index, item in enumerate(
            recommendations,
            start=1
        ):

            st.write(
                f"**{index}.** {item}"
            )

    else:

        st.info(
            "No recommendations extracted."
        )

    # ---------------------------------------------------------
    # PDF DOWNLOAD
    # ---------------------------------------------------------

    st.header("📄 Report Download")

    pdf_bytes = create_pdf(
        final_report
    )

    st.download_button(
        label="📥 Download PDF Report",
        data=pdf_bytes,
        file_name="resume_job_match_report.pdf",
        mime="application/pdf"
    )

    # ---------------------------------------------------------
    # FULL AGENT REPORT
    # ---------------------------------------------------------

    with st.expander(
        "📄 View Full Agent Report"
    ):

        st.markdown(
            final_report
        )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "AI Resume & Job Match Agent | "
    "Gemini + LangChain + LangGraph + Python"
)