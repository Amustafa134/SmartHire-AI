import re
import docx
import pdfplumber
from typing import List, Dict


# -----------------------------
# 1. FILE TEXT EXTRACTION
# -----------------------------

def extract_text(file_path: str) -> str:
    """
    Extracts raw text from PDF, DOCX, or TXT.
    """
    if file_path.lower().endswith(".pdf"):
        return extract_pdf(file_path)

    if file_path.lower().endswith(".docx"):
        return extract_docx(file_path)

    # fallback for .txt or unknown formats
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def extract_pdf(path: str) -> str:
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text += page_text + "\n"
    return text


def extract_docx(path: str) -> str:
    doc = docx.Document(path)
    return "\n".join(p.text for p in doc.paragraphs)


# -----------------------------
# 2. BASIC REGEX HELPERS
# -----------------------------

EMAIL_REGEX = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
PHONE_REGEX = r"(\+?\d{1,3}[\s-]?)?\d{10,12}"

SKILL_KEYWORDS = [
    "python", "java", "javascript", "c++", "sql", "html", "css",
    "machine learning", "deep learning", "tensorflow", "pytorch",
    "data analysis", "bioinformatics", "linux", "docker", "aws",
    "react", "node", "fastapi"
]

EDU_KEYWORDS = ["bachelor", "master", "phd", "university", "college", "degree"]

EXP_KEYWORDS = ["experience", "worked", "responsible", "intern", "project"]


# -----------------------------
# 3. INFO EXTRACTION FUNCTIONS
# -----------------------------

def extract_email(text: str):
    match = re.search(EMAIL_REGEX, text)
    return match.group(0).strip() if match else None


def extract_phone(text: str):
    match = re.search(PHONE_REGEX, text)
    return match.group(0).strip() if match else None


def extract_name(text: str):
    """
    Very simple name extractor: top line + capitalized words.
    """
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    if not lines:
        return None

    first_line = lines[0]
    if 2 <= len(first_line.split()) <= 4:
        return first_line

    return None


def extract_skills(text: str) -> List[str]:
    text_lower = text.lower()
    found = [s for s in SKILL_KEYWORDS if s in text_lower]
    return sorted(list(set(found)))


def extract_education(text: str) -> List[str]:
    lines = text.lower().split("\n")
    edu = [l.strip() for l in lines if any(e in l for e in EDU_KEYWORDS)]
    return edu


def extract_experience(text: str) -> List[str]:
    lines = text.lower().split("\n")
    exp = [l.strip() for l in lines if any(e in l for e in EXP_KEYWORDS)]
    return exp


# -----------------------------
# 4. MAIN PARSER
# -----------------------------

def parse_cv(file_path: str) -> Dict:
    """
    Main function → takes file path and outputs structured JSON.
    """

    raw_text = extract_text(file_path)

    data = {
        "name": extract_name(raw_text),
        "email": extract_email(raw_text),
        "phone": extract_phone(raw_text),
        "skills": extract_skills(raw_text),
        "education": extract_education(raw_text),
        "experience": extract_experience(raw_text),
        "raw_text": raw_text,
    }

    return data
