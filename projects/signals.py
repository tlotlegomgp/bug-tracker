import random
import string
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from index.models import Alert
from .models import Project, ProjectRole


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
        alert_url = f'/projects/{instance.project.slug}/'

        if instance.user_role == "Project Manager":
            alert_message = action_user + " assigned you as Project Manager to project, " + project_name + "."
        else:
            alert_message = action_user + " added you to project, " + project_name + "."

        if instance.project.created_by != instance.user:
            alert = Alert.objects.create(user=alert_user, note=alert_message, url=alert_url)


pre_save.connect(pre_save_project_receiver, sender=Project)
post_save.connect(projectrole_post_save_receiver, sender=ProjectRole)
