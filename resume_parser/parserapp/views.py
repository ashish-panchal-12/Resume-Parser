from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Job, Resume
from .forms import JobForm, ResumeUploadForm
from .utils.parser import parse_resume
from .utils.scoring import compute_score
from django.db.models import Avg
from django.views.decorators.http import require_POST
from django.contrib import messages
import re
import os



def dashboard(request):
    jobs = Job.objects.all()
    resumes = Resume.objects.all()
    avg_score = resumes.aggregate(Avg('score'))['score__avg'] or 0
    top_resumes = resumes.order_by('-score')[:5]

    context = {
        "total_jobs": jobs.count(),
        "total_resumes": resumes.count(),
        "avg_score": round(avg_score, 2),
        "top_resumes": top_resumes,
    }
    return render(request, "parserapp/dashboard.html", context)

def home(request):
    jobs = Job.objects.all().order_by('-id')
    return render(request, "parserapp/home.html", {"jobs": jobs})


def add_job(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = JobForm()
    return render(request, "parserapp/add_job.html", {"form": form})

def upload_resume(request):
    if request.method == "POST":
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)

            # Save file first so that file.path exists
            resume.save()

            # Now parse the file
            parsed_data = parse_resume(resume.file.path)
            resume.parsed_data = parsed_data

            # Compute ATS score if job selected
            if resume.job:
                resume.score = compute_score(resume.parsed_data, resume.job) # parsed_data , resume.job

            resume.save()
            return redirect(reverse("resume_detail", args=[resume.pk]))
    else:
        form = ResumeUploadForm()

    return render(request, "parserapp/upload.html", {"form": form})


def resume_detail(request, pk):
    resume = get_object_or_404(Resume, pk=pk)
    return render(request, "parserapp/resume_detail.html", {"resume": resume})


def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    resumes = Resume.objects.filter(job=job).order_by('-score')
    return render(request, "parserapp/job_detail.html", {"job": job, "resumes": resumes})

    text = ""

    # Read file text (PDF/DOCX/TXT)
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        from PyPDF2 import PdfReader
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() or ""
    elif ext == ".docx":
        from docx import Document
        doc = Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    else:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()

    # Normalize text
    text = re.sub(r"\s+", " ", text)

    # Extract email
    email_pattern = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
    emails = email_pattern.findall(text)
    email = emails[0] if emails else "Not Found"

    # Extract phone (supports +91, (), -, spaces, etc.)
    phone_pattern = re.compile(
        r"(?:(?:\+?\d{1,3}[\s-]*)?(?:\(?\d{2,4}\)?[\s-]*)?\d{6,10})"
    )
    phones = phone_pattern.findall(text)
    phone = None
    for p in phones:
        clean_p = re.sub(r"[^\d+]", "", p)
        if 8 <= len(clean_p) <= 13:
            phone = p.strip()
            break
    if not phone:
        phone = "Not Found"

    # Try to extract candidate name
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    possible_name = lines[0] if lines else os.path.basename(file_path).split(".")[0]
    name = " ".join(word.capitalize() for word in possible_name.split()[:3])

    # Extract simple skills (extendable)
    skills_list = [
        "python", "django", "flask", "javascript", "react", "java", "c++", "html",
        "css", "sql", "excel", "power bi", "aws", "git", "linux", "node", "angular",
        "tensorflow", "pytorch", "data analysis", "machine learning"
    ]
    found_skills = [s for s in skills_list if re.search(rf"\b{s}\b", text, re.I)]

    #  Construct parsed data
    parsed_data = {
        "name": name,
        "email": email,
        "phone": phone,
        "skills": found_skills,
    }

    return parsed_data

