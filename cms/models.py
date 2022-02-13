from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator


class User(AbstractUser):
    is_pu = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)
    organization_name = models.CharField(max_length=256)


class Company(models.Model):
    def __str__(self):
        return self.user.organization_name

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


class PU(models.Model):
    def __str__(self):
        return self.user.organization_name

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


class Profile(models.Model):
    pu = models.ForeignKey(PU, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    picture = models.ImageField()
    university = models.CharField(max_length=256)
    qualifications = models.TextField()
    skills = models.TextField()
    gpa = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    about = models.TextField()


class Job(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    position = models.CharField(max_length=256)
    salary = models.FloatField(default=0, validators=[MinValueValidator(0)])
    vacancy = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return self.position.replace(' ', '_')


class ShortListCandidates(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
