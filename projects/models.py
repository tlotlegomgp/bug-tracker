from django.db import models
from index.models import Profile


# Create your models here.


class Project(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200)
    created_on = models.DateTimeField(verbose_name="date created", auto_now_add=True)
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name


class ProjectRole(models.Model):

    ROLE = (
        ('Admin', 'Admin'),
        ('Project Manager', 'Project Manager'),
        ('Developer', 'Developer'),
        ('Submitter', 'Submitter'),
        ('Unassigned', 'Unassigned'),
    )

    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user_role = models.CharField(max_length=20, choices=ROLE, default='Un-assigned')
    created_on = models.DateTimeField(verbose_name="date added", auto_now_add=True)

    def __str__(self):
        return self.user_role
