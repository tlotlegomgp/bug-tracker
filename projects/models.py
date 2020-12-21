from django.db import models
from django.conf import settings
from index.models import Profile
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200)
    created_on = models.DateTimeField(verbose_name="date created", auto_now_add=True)
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ProjectRole(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=25, blank=True)
    created_on = models.DateTimeField(verbose_name="date added", auto_now_add=True)

    def __str__(self):
        return self.role


def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
    

def pre_save_project_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name + "-" + rand_slug())
    
pre_save.connect(pre_save_project_receiver, sender = Project)