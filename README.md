# AI Resume & Job Match Agent

An AI-powered resume-to-job matching system that analyzes a candidate's resume against a job description and generates a structured match report.

The system uses Google Gemini for understanding resume and job-description content, LangChain and LangGraph for the agent workflow, and deterministic Python-based scoring for evaluating the candidate-job match.



## Overview

Finding out whether a resume matches a particular job often requires manually comparing skills, education, experience, projects, and job requirements.

This project automates that process.

The application:

1. Accepts a resume PDF and job description.
2. Extracts information from the resume.
3. Uses Gemini to structure the resume and job description.
4. Matches the candidate's skills with job requirements.
5. Calculates multiple matching scores.
6. Identifies missing skills and gaps.
7. Generates recommendations.
8. Produces a final match report.
9. Displays the results through a Streamlit dashboard.
10. Allows the user to download the report as a PDF.


## Features

- 📄 Upload and extract text from resume PDFs
- 🤖 Analyze resumes using Google Gemini
- 💼 Analyze job descriptions using Google Gemini
- 🎯 Match required and preferred skills
- ⚠️ Identify missing skills and requirements
- 📊 Calculate multiple resume-job match scores
- 💡 Generate personalized recommendations
- 📑 Generate a structured match report
- 📈 Visualize score breakdowns
- 🖥️ Interactive Streamlit dashboard
- 📥 Download the final report as a PDF
- 🔗 LangChain tools for modular AI-agent functionality
- 🔄 LangGraph workflow for orchestrating the analysis pipeline


## How It Works

The system separates AI-based understanding from deterministic evaluation.

### Gemini handles

- Resume understanding
- Resume information extraction
- Job-description understanding
- Job requirement extraction
- Important keyword identification


## Python-based components handle

- Skill matching
- Experience comparison
- Education comparison
- Project comparison
- Keyword scoring
- Overall score calculation
- Recommendations
- Final report generation


## System Architecture

┌────────────────────┐
│        User               │
└────────────────────┘
           │
           ▼
┌────────────────────┐
│  Streamlit Web App        │
└────────────────────┘
           │
           ▼
┌────────────────────┐
│   Resume PDF +            │
│   Job Description         │
└────────────────────┘
           │
           ▼
┌────────────────────┐
│    Resume Parser         │
│     (PyMuPDF)            │
└────────────────────┘
           │
           ▼
┌────────────────────────────┐
│      Gemini Analysis                │
│                                     │
│  Resume Analysis                    │
│  Job Description Analysis           │
└────────────────────────────┘
           │
           ▼
┌───────────────────┐
│   Skill Matching        │
└───────────────────┘
           │
           ▼
┌───────────────────┐
│   Score Calculation     │
│                         │
│ Skills                  │
│ Experience              │
│ Education               │
│ Projects                │
│ Keywords                │
└───────────────────┘
           │
           ▼
┌────────────────────┐
│  Recommendations          │
└────────────────────┘
           │
           ▼
┌────────────────────┐
│    Match Report           │
└────────────────────┘
           │
           ▼
┌─────────────────────────────┐
│       Final Results                   │
│                                       │
│ Overall Score                         │
│ Score Breakdown                       │
│ Skill Gaps                            │
│ Recommendations                       │
│ PDF Report                            │
└─────────────────────────────┘