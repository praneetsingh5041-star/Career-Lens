import re
from pathlib import Path

SKILL_ALIASES = {
    "python": ["python"],
    "java": ["java"],
    "c++": ["c++", "cpp"],
    "sql": ["sql", "mysql", "postgresql", "sqlite"],
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning"],
    "data analysis": ["data analysis", "data analytics"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch", "torch"],
    "nlp": ["natural language processing", "nlp"],
    "computer vision": ["computer vision", "opencv"],
    "excel": ["excel", "microsoft excel"],
    "power bi": ["power bi"],
    "tableau": ["tableau"],
    "statistics": ["statistics", "statistical"],
    "data visualization": ["data visualization", "visualization"],
    "html": ["html"],
    "css": ["css"],
    "javascript": ["javascript", "js"],
    "flask": ["flask"],
    "django": ["django"],
    "streamlit": ["streamlit"],
    "git": ["git", "github"],
    "cloud": ["cloud", "aws", "azure", "gcp"],
    "communication": ["communication", "presentation"],
    "problem solving": ["problem solving", "problem-solving"],
    "teamwork": ["teamwork", "collaboration"],
    "linux": ["linux"],
    "api": ["api", "rest api", "restful"],
}

CAREER_MAP = {
    "Data Analyst": {"sql","python","excel","power bi","tableau","statistics","data analysis","data visualization"},
    "Machine Learning Intern": {"python","machine learning","pandas","numpy","scikit-learn","statistics"},
    "NLP Intern": {"python","nlp","machine learning","deep learning"},
    "Computer Vision Intern": {"python","computer vision","deep learning","opencv"},
    "Python Developer": {"python","sql","flask","django","api","git"},
    "Frontend Developer": {"html","css","javascript","git"},
    "AI Engineer Intern": {"python","machine learning","deep learning","pytorch","tensorflow","api"},
}

def _contains_phrase(text, phrase):
    # Avoid false matches such as "java" inside "javascript".
    pattern = r"(?<![a-zA-Z0-9+#])" + re.escape(phrase) + r"(?![a-zA-Z0-9+#])"
    return bool(re.search(pattern, text, flags=re.IGNORECASE))

def extract_skills(text):
    found = []
    for canonical, aliases in SKILL_ALIASES.items():
        if any(_contains_phrase(text, alias) for alias in aliases):
            found.append(canonical)
    return sorted(set(found))

def analyze_resume(resume_text, job_description):
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)
    matched = sorted(set(resume_skills) & set(job_skills))
    missing = sorted(set(job_skills) - set(resume_skills))
    score = round((len(matched) / len(job_skills)) * 100) if job_skills else 0

    suggestions = []
    if not resume_skills:
        suggestions.append("Add a clearly labeled Skills section using skills you genuinely have.")
    if missing:
        suggestions.append("Consider learning or demonstrating: " + ", ".join(missing[:8]) + ".")
    if "project" not in resume_text.lower():
        suggestions.append("Add 1–2 relevant projects with your role, tools, and measurable outcome.")
    if "intern" in job_description.lower() or "entry" in job_description.lower():
        suggestions.append("Highlight coursework, internships, certifications, and academic projects relevant to the role.")
    if not any(k in resume_text.lower() for k in ["github", "portfolio", "linkedin"]):
        suggestions.append("Include a portfolio, GitHub, or LinkedIn link if you have one.")
    if not suggestions:
        suggestions.append("Keep tailoring experience bullets to the role and quantify outcomes where possible.")

    role_scores = []
    resume_set = set(resume_skills)
    for role, role_skills in CAREER_MAP.items():
        overlap = len(resume_set & role_skills)
        if role_skills:
            role_scores.append((role, overlap / len(role_skills)))
    recommendations = [role for role, score_ in sorted(role_scores, key=lambda x:x[1], reverse=True)[:3] if score_ > 0]

    return {
        "match_score": score,
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matched_skills": matched,
        "missing_skills": missing,
        "suggestions": suggestions,
        "career_recommendations": recommendations,
    }

def extract_text_from_pdf(uploaded_file):
    import fitz
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    return "\n".join(page.get_text() for page in doc)

def extract_text_from_docx(uploaded_file):
    from docx import Document
    doc = Document(uploaded_file)
    return "\n".join(p.text for p in doc.paragraphs)

def demo_resume():
    return """Praneet Singh
CSE Artificial Intelligence student
Skills: Python, SQL, Pandas, NumPy, Machine Learning, Data Analysis, Statistics, Excel, Git
Projects:
Student performance dashboard using Python and Pandas.
Resume analyzer prototype using NLP keyword matching.
Coursework: Data Structures, Database Management, Machine Learning.
GitHub portfolio and communication skills."""

def demo_job():
    return """Data Analyst Intern
Required skills: Python, SQL, Excel, Power BI, Pandas, NumPy, Statistics, Data Analysis, Data Visualization.
Responsibilities: clean data, build dashboards, analyze trends, communicate insights.
Preferred: Git and problem solving."""
