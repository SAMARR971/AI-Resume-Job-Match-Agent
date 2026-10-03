from src.resume_parser import extract_resume_text


pdf_path = "data/test_resume.pdf"

resume_text = extract_resume_text(pdf_path)

print("=" * 60)
print("EXTRACTED RESUME")
print("=" * 60)

print(resume_text)