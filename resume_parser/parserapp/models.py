from django.db import models
from django.utils import timezone

class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    required_skills = models.TextField(help_text="Comma-separated skills")
    min_experience = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Resume(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to='resumes/')
    parsed_data = models.JSONField(default=dict, blank=True)
    score = models.FloatField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resume {self.id} - {self.job.title if self.job else 'Unassigned'}"