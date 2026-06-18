import re
import os
from PyPDF2 import PdfReader
from docx import Document


def extract_text_from_file(file_path):
    """
    Extracts raw text from PDF, DOCX, or TXT file.
    """
    text = ""
    ext = os.path.splitext(file_path)[1].lower()

    try:
        if ext == ".pdf":
            reader = PdfReader(file_path)
            for page in reader.pages:
                text += page.extract_text() or ""
        elif ext == ".docx":
            doc = Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        else:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")

    return re.sub(r"\s+", " ", text).strip()


def extract_email(text):
    """
    Extracts first email found in the text.
    """
    email_pattern = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
    matches = email_pattern.findall(text)
    return matches[0] if matches else "Not Found"


def extract_phone(text):
    """
    Extracts first valid phone number found in text.
    Supports +91, spaces, parentheses, dashes, etc.
    """
    phone_pattern = re.compile(
        r"(?:(?:\+?\d{1,3}[\s\-]*)?(?:\(?\d{2,4}\)?[\s\-]*)?\d{6,10})"
    )
    matches = phone_pattern.findall(text)
    for m in matches:
        clean = re.sub(r"[^\d+]", "", m)
        if 8 <= len(clean) <= 13:
            return m.strip()
    return "Not Found"


def extract_name(file_path, text):
    """
    Tries to extract the candidate's name from the first line or filename.
    """
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    if lines:
        first_line = lines[0]
        if 3 <= len(first_line.split()) <= 4 and not re.search(r"\d", first_line):
            return " ".join(word.capitalize() for word in first_line.split())
    # Fallback: use file name
    base_name = os.path.basename(file_path).split(".")[0]
    return " ".join(word.capitalize() for word in base_name.split("_")[:3])


def extract_skills(text):
    """
    Matches common technical and professional skills.
    """
    skills_list = [
        "python", "django", "flask", "javascript", "react", "angular", "vue",
        "java", "c++", "c#", "html", "css", "sql", "mysql", "postgresql", "mongodb",
        "aws", "git", "linux", "docker", "kubernetes", "excel", "power bi",
        "tensorflow", "pytorch", "machine learning", "data analysis", "node", "api"
    ]
    found = [s for s in skills_list if re.search(rf"\b{s}\b", text, re.I)]
    return sorted(list(set(found)))


def parse_resume(file_path):
    """
    Main function: orchestrates resume parsing.
    Returns structured data + full resume text.
    """
    text = extract_text_from_file(file_path)
    email = extract_email(text)
    phone = extract_phone(text)
    name = extract_name(file_path, text)
    skills = extract_skills(text)

    parsed_data = {
        "name": name,
        "email": email,
        "phone": phone,
        "skills": skills,
        "text_preview": text.strip(),
    }

    return parsed_data