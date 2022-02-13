from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import User, PU, Company, Profile, Job, ShortListCandidates


class EmpSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'organization_name', 'first_name', 'last_name', 'email', 'password1', 'password2')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_pu = True
        user.save()
        employee = PU.objects.create(user=user)
        employee.save()
        return user


class CompSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'organization_name', 'first_name', 'last_name', 'email', 'password1', 'password2')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_company = True
        user.save()
        company = Company.objects.create(user=user)
        company.save()
        return user


class AddProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'picture', 'qualifications', 'skills', 'gpa', 'about']


class AddJobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['position', 'salary', 'vacancy']


class ShortlistForm(forms.ModelForm):
    class Meta:
        model = ShortListCandidates
        fields = ['company', 'profile']
