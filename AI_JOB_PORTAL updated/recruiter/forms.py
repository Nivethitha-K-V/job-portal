from django import forms
from .models import Company

FORM_CONTROL = {'class': 'form-control'}


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['company_name', 'logo', 'website', 'industry', 'company_size', 'about', 'location']
        widgets = {
            'company_name': forms.TextInput(attrs=FORM_CONTROL),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs=FORM_CONTROL),
            'industry': forms.TextInput(attrs=FORM_CONTROL),
            'company_size': forms.TextInput(attrs=FORM_CONTROL),
            'about': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'location': forms.TextInput(attrs=FORM_CONTROL),
        }
