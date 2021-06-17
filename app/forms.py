from django import forms
from django.contrib.auth.models import User

from app.models import Company, Project, Employee


class CompanyForm(forms.ModelForm):
    logo_img = forms.ImageField(required=False)

    class Meta:
        model = Company
        fields = ['logo_img', 'name', 'city', 'description', 'site', 'phone', 'email', 'telegram']


class ProjectForm(forms.ModelForm):
    logo_img = forms.ImageField(required=False)
    company = forms.ModelChoiceField(queryset=Company.objects.all())

    class Meta:
        model = Project
        fields = ['logo_img', 'name', 'description', 'company']


class EmployeeForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all())
    company = forms.ModelChoiceField(queryset=Company.objects.all())

    class Meta:
        model = Employee
        fields = ['company', 'user', 'role']
