import random
import string
from django.db import models
from index.models import Profile
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.dispatch import receiver


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
        ('Member', 'Member'),
    )

    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user_role = models.CharField(max_length=20, choices=ROLE, default='MEM')
    created_on = models.DateTimeField(verbose_name="date added", auto_now_add=True)

    def __str__(self):
        return self.user_role


def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))


def pre_save_project_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name + "-" + rand_slug())


pre_save.connect(pre_save_project_receiver, sender=Project)
