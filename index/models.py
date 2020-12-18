from django.db import models
from django.conf import settings
from account.models import Profile
# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=15, unique=True)
    description = models.CharField(max_length=100)
    created_on = models.DateTimeField(verbose_name="date created", auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Ticket(models.Model):

    TICKET_PRIORITY = (
        ('NONE', 'None'),
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    )

    TICKET_STATUS = (
        ('NEW', 'New'),
        ('IN_PROGRESS', 'In_Progress'),
        ('RESOLVED', 'Resolved'),
    )

    TICKET_TYPE = (
        ('TASK', 'Task'),
        ('BUG', 'Bug'),
        ('CHANGE', 'Change'),
        ('FEATURE', 'Feature_request')
    )

    title = models.CharField(max_length=15)
    description = models.CharField(max_length=40)
    assigned_to = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_on = models.DateTimeField(verbose_name="created_on", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="date updated", auto_now=True)
    priority = models.CharField(max_length=12, choices=TICKET_PRIORITY, default='NONE')
    status = models.CharField(max_length=12, choices=TICKET_STATUS, default='NEW')
    class_type = models.CharField(max_length=12, choices=TICKET_TYPE, default='TASK')


class ProjectRole(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=15)
    created_on = models.DateTimeField(verbose_name="date added", auto_now_add=True)


class TicketComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    created_on = models.DateTimeField(verbose_name="date created", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="date updated", auto_now=True)
    body_message = models.CharField(max_length=50)


class TicketAttachment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    submitted_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_on = models.DateTimeField(verbose_name="created on", auto_now_add=True)
    note = models.CharField(max_length=30)
    attachment = models.FileField()


class Todo(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_on = models.DateTimeField(verbose_name="created on", auto_now_add=True)
    note = models.CharField(max_length=30)
