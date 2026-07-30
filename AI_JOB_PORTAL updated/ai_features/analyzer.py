"""
Rule-based AI-style resume analyzer and skill gap engine.

This module extracts text from an uploaded PDF resume, matches it against a
curated skill dictionary, and produces a score, detected/missing skills,
strengths, weaknesses, and improvement suggestions. It also compares a
candidate's stored skills against a job's required skills for the Skill Gap
Analyzer.

No external AI API is called here — everything runs locally so the feature
works offline. You can later swap `extract_resume_text` + `score_resume`
internals for a call to an LLM API if you want richer analysis.
"""

import re
from PyPDF2 import PdfReader

# Curated skill dictionary grouped by category — expand this as needed.
SKILL_DICTIONARY = {
    'Programming': ['python', 'java', 'c++', 'c#', 'javascript', 'typescript', 'go', 'ruby', 'php', 'sql'],
    'Web': ['django', 'flask', 'react', 'angular', 'vue', 'node.js', 'html', 'css', 'bootstrap', 'rest api'],
    'Data': ['pandas', 'numpy', 'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'data analysis', 'nlp'],
    'Cloud/DevOps': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'ci/cd', 'git', 'linux'],
    'Database': ['mysql', 'postgresql', 'mongodb', 'sqlite', 'oracle'],
    'Soft Skills': ['communication', 'leadership', 'teamwork', 'problem solving', 'time management'],
}

ALL_SKILLS = [skill for group in SKILL_DICTIONARY.values() for skill in group]

COURSE_SUGGESTIONS = {
    'python': 'Python for Everybody (Coursera)',
    'django': 'Django for Beginners (djangoforbeginners.com)',
    'react': 'React – The Complete Guide (Udemy)',
    'sql': 'SQL for Data Science (Coursera)',
    'machine learning': 'Machine Learning by Andrew Ng (Coursera)',
    'aws': 'AWS Cloud Practitioner Essentials',
    'docker': 'Docker & Kubernetes: The Practical Guide (Udemy)',
    'git': 'Git & GitHub Crash Course',
    'javascript': 'The Complete JavaScript Course (Udemy)',
    'data analysis': 'Data Analysis with Python (freeCodeCamp)',
}


def extract_resume_text(file_field):
    """Extract raw text from an uploaded PDF FieldFile."""
    text = ''
    try:
        file_field.open('rb')
        reader = PdfReader(file_field)
        for page in reader.pages:
            page_text = page.extract_text() or ''
            text += page_text + '\n'
    finally:
        file_field.close()
    return text.lower()


def detect_skills(text):
    found = []
    for skill in ALL_SKILLS:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text):
            found.append(skill)
    return sorted(set(found))


def analyze_resume(resume_file):
    """
    Returns a dict: score, skills_detected, missing_skills, strengths,
    weaknesses, suggestions.
    """
    text = extract_resume_text(resume_file)
    detected = detect_skills(text)
    missing = sorted(set(ALL_SKILLS) - set(detected))

    word_count = len(text.split())

    # --- Scoring heuristic (0-100) ---
    score = 0
    score += min(len(detected) * 4, 40)          # up to 40 pts for skill breadth
    if 'experience' in text or 'internship' in text:
        score += 15
    if 'project' in text:
        score += 15
    if re.search(r'\b(b\.?tech|bachelor|degree|university|college)\b', text):
        score += 10
    if 'email' in text or re.search(r'[\w.-]+@[\w.-]+', text):
        score += 5
    if word_count > 150:
        score += 10
    if any(s in detected for s in SKILL_DICTIONARY['Soft Skills']):
        score += 5
    score = min(score, 100)

    # --- Strengths ---
    strengths = []
    if len(detected) >= 6:
        strengths.append("Strong and diverse technical skill set.")
    if 'project' in text:
        strengths.append("Includes project experience, which recruiters value highly.")
    if re.search(r'[\w.-]+@[\w.-]+', text):
        strengths.append("Contact details are present and easy to find.")
    if not strengths:
        strengths.append("Resume successfully parsed — basic structure is in place.")

    # --- Weaknesses ---
    weaknesses = []
    if word_count < 150:
        weaknesses.append("Resume content looks quite short — consider adding more detail.")
    if 'project' not in text:
        weaknesses.append("No clear project section detected.")
    if len(detected) < 4:
        weaknesses.append("Few recognizable technical skills found — list your skills explicitly.")
    if not re.search(r'[\w.-]+@[\w.-]+', text):
        weaknesses.append("No email address detected — make sure contact info is visible as text (not an image).")
    if not weaknesses:
        weaknesses.append("No major issues detected — nice work!")

    # --- Suggestions ---
    suggestions = []
    if missing:
        top_missing = missing[:5]
        suggestions.append(f"Consider adding in-demand skills such as: {', '.join(top_missing)}.")
    suggestions.append("Quantify achievements with numbers where possible (e.g. 'improved performance by 20%').")
    suggestions.append("Keep formatting simple — avoid tables/columns that PDF parsers may misread.")
    if 'certification' not in text and 'certificate' not in text:
        suggestions.append("Add relevant certifications to strengthen credibility.")

    return {
        'score': score,
        'skills_detected': detected,
        'missing_skills': missing[:15],
        'strengths': strengths,
        'weaknesses': weaknesses,
        'suggestions': suggestions,
    }


def analyze_skill_gap(candidate_skill_names, job_skills_required):
    """
    candidate_skill_names: list[str] from the candidate's Skill model
    job_skills_required: list[str] parsed from Job.skills_required
    """
    candidate_set = {s.strip().lower() for s in candidate_skill_names if s.strip()}
    job_set = {s.strip().lower() for s in job_skills_required if s.strip()}

    if not job_set:
        return {'match_percentage': 0, 'missing_skills': [], 'matched_skills': [], 'recommended_courses': []}

    matched = job_set & candidate_set
    missing = sorted(job_set - candidate_set)
    match_percentage = round((len(matched) / len(job_set)) * 100)

    recommended_courses = []
    for skill in missing:
        course = COURSE_SUGGESTIONS.get(skill)
        if course:
            recommended_courses.append(f"{skill.title()}: {course}")
        else:
            recommended_courses.append(f"{skill.title()}: search for a beginner course on Coursera/Udemy")

    return {
        'match_percentage': match_percentage,
        'matched_skills': sorted(matched),
        'missing_skills': missing,
        'recommended_courses': recommended_courses,
    }
