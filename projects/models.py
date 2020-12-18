from django.db import models
from django.conf import settings
from index.models import Profile

# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200)
    created_on = models.DateTimeField(verbose_name="date created", auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class ProjectRole(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=25)
    created_on = models.DateTimeField(verbose_name="date added", auto_now_add=True)