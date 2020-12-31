import os
from django.db import models
from account.models import Profile
from projects.models import Project

# Create your models here.


class Ticket(models.Model):

    TICKET_PRIORITY = (
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    )

    TICKET_STATUS = (
        ('NEW', 'New'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
    )

    TICKET_TYPE = (
        ('TASK', 'Task'),
        ('BUG', 'Bug'),
        ('CHANGE', 'Change'),
        ('FEATURE', 'Feature request')
    )

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name="tickets", on_delete=models.CASCADE)
    created_on = models.DateTimeField(verbose_name="created_on", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="date updated", auto_now=True)
    priority = models.CharField(max_length=12, choices=TICKET_PRIORITY, default='LOW')
    status = models.CharField(max_length=12, choices=TICKET_STATUS, default='NEW')
    class_type = models.CharField(max_length=12, choices=TICKET_TYPE, default='TASK')
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.title


class TicketAssignee(models.Model):

    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    created_on = models.DateTimeField(verbose_name="date created", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="date updated", auto_now=True)

    def __str__(self):
        return self.user.user.email + " " + self.ticket.title


class TicketComment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    created_on = models.DateTimeField(verbose_name="date created", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="date updated", auto_now=True)
    body_message = models.CharField(max_length=100)

    def __str__(self):
        return self.body_message


class TicketAttachment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_on = models.DateTimeField(verbose_name="created on", auto_now_add=True)
    note = models.CharField(max_length=100)
    attachment = models.FileField(upload_to='ticket_attachments')

    def __str__(self):
        return self.note

    def filename(self):
        return os.path.basename(self.attachment.name)
