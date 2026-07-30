from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile, Education, Skill, Resume

FORM_CONTROL = {'class': 'form-control'}


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs=FORM_CONTROL))
    full_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs=FORM_CONTROL))
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    username = forms.CharField(widget=forms.TextInput(attrs=FORM_CONTROL))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=FORM_CONTROL))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=FORM_CONTROL))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                full_name=self.cleaned_data['full_name'],
                role=self.cleaned_data['role'],
            )
        return user


class StyledLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs=FORM_CONTROL))
    password = forms.CharField(widget=forms.PasswordInput(attrs=FORM_CONTROL))


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'full_name', 'mobile', 'profile_photo', 'gender', 'date_of_birth',
            'state', 'city', 'address', 'pincode',
            'linkedin_url', 'github_url', 'portfolio_url',
            'experience_years', 'experience_summary',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs=FORM_CONTROL),
            'mobile': forms.TextInput(attrs=FORM_CONTROL),
            'profile_photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'state': forms.TextInput(attrs=FORM_CONTROL),
            'city': forms.TextInput(attrs=FORM_CONTROL),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'pincode': forms.TextInput(attrs=FORM_CONTROL),
            'linkedin_url': forms.URLInput(attrs=FORM_CONTROL),
            'github_url': forms.URLInput(attrs=FORM_CONTROL),
            'portfolio_url': forms.URLInput(attrs=FORM_CONTROL),
            'experience_years': forms.NumberInput(attrs=FORM_CONTROL),
            'experience_summary': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['qualification', 'college', 'degree', 'branch', 'passing_year', 'cgpa', 'percentage']
        widgets = {
            'qualification': forms.Select(attrs={'class': 'form-select'}),
            'college': forms.TextInput(attrs=FORM_CONTROL),
            'degree': forms.TextInput(attrs=FORM_CONTROL),
            'branch': forms.TextInput(attrs=FORM_CONTROL),
            'passing_year': forms.NumberInput(attrs=FORM_CONTROL),
            'cgpa': forms.NumberInput(attrs=FORM_CONTROL),
            'percentage': forms.NumberInput(attrs=FORM_CONTROL),
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'skill_type', 'proficiency']
        widgets = {
            'name': forms.TextInput(attrs=FORM_CONTROL),
            'skill_type': forms.Select(attrs={'class': 'form-select'}),
            'proficiency': forms.NumberInput(attrs=FORM_CONTROL),
        }


class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
