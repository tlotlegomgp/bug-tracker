import random
import string
from django.shortcuts import get_object_or_404
from django.db import models
from index.models import Alert, Profile
from django.db.models.signals import pre_save, post_save
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
    user_role = models.CharField(max_length=20, choices=ROLE, default='Member')
    created_on = models.DateTimeField(verbose_name="date added", auto_now_add=True)

    def __str__(self):
        return self.user_role


def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))


def pre_save_project_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name + "-" + rand_slug())


def projectrole_post_save_receiver(sender, instance, created, **kwargs):
    if created:
        action_user = instance.project.created_by.first_name + " " + instance.project.created_by.last_name
        alert_user = instance.user
        project_name = instance.project.name

        if instance.user_role == "Project Manager":
            alert_message = action_user + " assigned you as Project Manager to project, " + project_name + "."
        else:
            alert_message = action_user + " added you to project, " + project_name + "."

        if instance.project.created_by != instance.user:
            alert = Alert.objects.create(user=alert_user, note=alert_message)


pre_save.connect(pre_save_project_receiver, sender=Project)
post_save.connect(projectrole_post_save_receiver, sender=ProjectRole)
