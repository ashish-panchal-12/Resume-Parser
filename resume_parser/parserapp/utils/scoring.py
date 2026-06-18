def compute_score(parsed_data, job):
    job_skills = [s.strip().lower() for s in job.required_skills.split(",")]
    # resume_text = parsed_data.get("raw_text", "").lower()
    resume_text = parsed_data.get("skills")

    matches = sum(1 for skill in job_skills if skill in resume_text)
    score = round((matches / len(job_skills)) * 100+20, 2) if job_skills else 0
    return score