from django.db import models
from account.models import Profile


# Create your models here.


class Todo(models.Model):
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_on = models.DateTimeField(verbose_name="created on", auto_now_add=True)
    note = models.CharField(max_length=50)

    def __str__(self):
        return self.note


class DirectMessage(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    receiver = models.ForeignKey(Profile, related_name="direct_messages", on_delete=models.CASCADE)
    created_on = models.DateTimeField(verbose_name="created on", auto_now_add=True)
    body = models.CharField(max_length=200)

    def __str__(self):
        return self.author.first_name + " " + self.author.last_name


class Alert(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_on = models.DateTimeField(verbose_name="created on", auto_now_add=True)
    note = models.CharField(max_length=150)

    def __str__(self):
        return self.note
