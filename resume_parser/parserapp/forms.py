from django import forms
from .models import Job, Resume

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ["title", "description", "required_skills", "min_experience"]


class ResumeUploadForm(forms.ModelForm):
    job = forms.ModelChoiceField(
        queryset=Job.objects.all(), required=False, label="Select Job (optional)"
    )

    class Meta:
        model = Resume
        fields = ["file", "job"]