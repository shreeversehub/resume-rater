import re

# ---------------- SAMPLE RESUME TEXT ----------------
resume_text = """
Lalitha Shree
Email: lalitha2005@gmail.com
Phone: 9025120284

Experience:
- 1 years at TCS
- 2 years at Amazon

Education:
- Anna University, Chennai

Skills:
Python, Machine Learning, Data Science, Communication, Leadership,c++,full stack developer,data analyist

Certifications:
AWS Certified Solutions Architect, Google Data Analytics Professional Certificate,python certificate
"""

# ---------------- SAMPLE JOB DESCRIPTION ----------------
job_description = """
We are looking for a Data Scientist with skills in Python, Machine Learning, and Data Science.
Experience with AWS, leadership, and analytics is a plus.
"""


# ---------------- FAKE DETECTION LOGIC ----------------
def detect_fake_resume(text):
    fake_signals = []
    exp_years = re.findall(r'(\d+)\s+years', text.lower())
    if exp_years and max(map(int, exp_years)) > 40:
        fake_signals.append("Unrealistic years of experience")
    words = text.split()
    if len(words) > 0 and (len(words) - len(set(words))) / len(words) > 0.4:
        fake_signals.append("Possible keyword stuffing")
    known_companies = ["google", "microsoft", "tcs", "infosys", "amazon"]
    companies = re.findall(r'at\s+([A-Z][a-zA-Z]+)', text)
    for comp in companies:
        if comp.lower() not in known_companies:
            fake_signals.append(f"Unrecognized company: {comp}")
    known_universities = ["harvard", "oxford", "stanford", "anna university"]
    if not any(uni in text.lower() for uni in known_universities):
        fake_signals.append("No recognized university mentioned")
    return fake_signals


# ---------------- MATCH RATING ----------------
def calculate_match_score(text, job_description):
    job_words = set(job_description.lower().split())
    resume_words = set(text.lower().split())
    matched_words = job_words.intersection(resume_words)
    score = (len(matched_words) / len(job_words)) * 100 if job_words else 0
    return round(score, 2)


# ---------------- EXTRACT CANDIDATE DETAILS ----------------
def extract_candidate_details(text):
    skills_match = re.findall(r"Skills:\s*(.*)", text)
    cert_match = re.findall(r"Certifications:\s*(.*)", text)
    edu_match = re.findall(r"Education:\s*(.*)", text)
    exp_match = re.findall(r"Experience:\s*(.*)", text)

    skills = skills_match[0] if skills_match else "Not Mentioned"
    certifications = cert_match[0] if cert_match else "Not Mentioned"
    education = edu_match[0] if edu_match else "Not Mentioned"
    experience = exp_match[0] if exp_match else "Not Mentioned"

    return skills, certifications, education, experience


# ---------------- COMPANY MATCH LOGIC ----------------
def company_suggestion(score, skills, certifications):
    if score >= 80 and "AWS" in certifications:
        return "MNC Company (High Demand)"
    elif score >= 60:
        return "Mid-level Tech Company"
    else:
        return "Startup or Entry-level Company"


# ---------------- SALARY ESTIMATION ----------------
def estimate_salary(company_type, experience_years):
    if company_type == "MNC Company (High Demand)":
        return f"₹12 - ₹20 LPA (Based on {experience_years} years of experience)"
    elif company_type == "Mid-level Tech Company":
        return f"₹6 - ₹12 LPA (Based on {experience_years} years of experience)"
    else:
        return f"₹3 - ₹6 LPA (Based on {experience_years} years of experience)"


# ---------------- MAIN ----------------
if __name__ == "__main__":
    print("=== Resume Analysis Report ===")

    score = calculate_match_score(resume_text, job_description)
    skills, certifications, education, experience = extract_candidate_details(resume_text)
    fake_flags = detect_fake_resume(resume_text)

    print(f"\nCandidate Skills: {skills}")
    print(f"Certifications: {certifications}")
    print(f"Education: {education}")
    print(f"Experience: {experience}")
    print(f"Match Score: {score}%")

    if fake_flags:
        print("\n⚠ Possible Fake Indicators:")
        for flag in fake_flags:
            print(f"- {flag}")
    else:
        print("\n✅ Resume appears genuine.")

    company_type = company_suggestion(score, skills, certifications)
    print(f"\nRecommended Company Type: {company_type}")

    exp_years = sum(map(int, re.findall(r'(\d+)\s+years', resume_text.lower())))
    salary_range = estimate_salary(company_type, exp_years)
    print(f"Estimated Salary Package: {salary_range}")

    print(f"\nReasoning: Based on the candidate's skills ({skills}), certifications ({certifications}), "
          f"and experience ({exp_years} years), this resume is best suited for a {company_type}. "
          f"The salary estimate is {salary_range}. The skills match the job description with {score}% similarity.")
