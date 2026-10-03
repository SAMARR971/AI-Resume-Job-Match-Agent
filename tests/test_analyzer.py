from src.resume_parser import extract_resume_text
from src.analyzer import analyze_resume


pdf_path = "data/test_resume.pdf"

# Extract text from the PDF
resume_text = extract_resume_text(pdf_path)

# Analyze the resume with Gemini
analysis = analyze_resume(resume_text)

print("=" * 60)
print("STRUCTURED RESUME ANALYSIS")
print("=" * 60)

for key, value in analysis.items():
    print(f"\n{key}:")
    print(value)