from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("jobs/", views.home, name="home"),
    path("job/add/", views.add_job, name="add_job"),
    path("upload/", views.upload_resume, name="upload_resume"),
    path("resume/<int:pk>/", views.resume_detail, name="resume_detail"),
    path("job/<int:pk>/", views.job_detail, name="job_detail"),
]