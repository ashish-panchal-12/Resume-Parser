# Resume Parser & ATS Scoring System

A Django-based web application that parses resumes, extracts candidate information, and calculates ATS (Applicant Tracking System) scores by matching candidate skills with job requirements.

## 🚀 Features

* Upload resumes in PDF and DOCX formats
* Extract candidate information automatically

  * Name
  * Email
  * Phone Number
  * Skills
* Create and manage job postings
* ATS score calculation based on required skills
* Rank candidates according to job fit
* Dashboard for viewing jobs and applicants
* Resume storage and management

## 🛠️ Tech Stack

* Python
* Django
* SQLite
* PyPDF2
* python-docx
* HTML
* CSS
* Bootstrap

## 📂 Project Structure

```text
Resume-Parser/
│
├── parserapp/
│   ├── templates/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── resume_parser/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── media/
├── manage.py
├── requirements.txt
└── README.md
```

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/ashish-panchal-12/Resume-Parser.git
cd Resume-Parser
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the virtual environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Apply migrations

```bash
python manage.py migrate
```

### Run the application

```bash
python manage.py runserver
```

Open your browser and visit:

```text
http://127.0.0.1:8000/
```

## 📊 ATS Scoring Logic

The ATS score is calculated by comparing the skills extracted from a resume with the required skills for a job posting.

```text
ATS Score = (Matched Skills / Required Skills) × 100
```

Higher scores indicate a better match between the candidate and the job requirements.

## 📄 Supported File Formats

* PDF (.pdf)
* DOCX (.docx)

## 🎯 Use Cases

* HR Recruitment Teams
* Resume Screening
* Candidate Ranking
* Skill Matching
* Recruitment Automation

## 🔮 Future Enhancements

* NLP-based skill extraction
* AI-powered resume analysis
* Resume keyword highlighting
* Authentication system
* Email notifications
* Export candidate reports

## 👨‍💻 Author

**Ashish Panchal**

GitHub: https://github.com/ashish-panchal-12

## 📜 License

This project is licensed under the MIT License.
