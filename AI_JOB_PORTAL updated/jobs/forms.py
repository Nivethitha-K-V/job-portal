from django import forms
from .models import Job

FORM_CONTROL = {'class': 'form-control'}
FORM_SELECT = {'class': 'form-select'}


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title', 'company', 'description', 'skills_required',
            'location', 'salary', 'job_type', 'experience',
        ]
        widgets = {
            'title': forms.TextInput(attrs=FORM_CONTROL),
            'company': forms.TextInput(attrs=FORM_CONTROL),
            'description': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'skills_required': forms.TextInput(attrs=FORM_CONTROL),
            'location': forms.TextInput(attrs=FORM_CONTROL),
            'salary': forms.TextInput(attrs=FORM_CONTROL),
            'job_type': forms.Select(attrs=FORM_SELECT),
            'experience': forms.Select(attrs=FORM_SELECT),
        }


class JobSearchForm(forms.Form):
    keyword = forms.CharField(required=False, widget=forms.TextInput(attrs={**FORM_CONTROL, 'placeholder': 'Job title, company, or skill'}))
    location = forms.CharField(required=False, widget=forms.TextInput(attrs={**FORM_CONTROL, 'placeholder': 'Location'}))
    job_type = forms.ChoiceField(
        required=False,
        choices=(('', 'Any Type'),) + Job.JOB_TYPE_CHOICES,
        widget=forms.Select(attrs=FORM_SELECT),
    )
    experience = forms.ChoiceField(
        required=False,
        choices=(('', 'Any Experience'),) + Job.EXPERIENCE_CHOICES,
        widget=forms.Select(attrs=FORM_SELECT),
    )
