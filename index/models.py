from django.db import models
from django.conf import settings
from account.models import Profile
from projects.models import Project, ProjectRole
# Create your models here.


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

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    assigned_to = models.ForeignKey(Profile, related_name="user_tickets", on_delete=models.CASCADE)
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name="tickets", on_delete=models.CASCADE)
    created_on = models.DateTimeField(verbose_name="created_on", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="date updated", auto_now=True)
    priority = models.CharField(max_length=12, choices=TICKET_PRIORITY, default='NONE')
    status = models.CharField(max_length=12, choices=TICKET_STATUS, default='NEW')
    class_type = models.CharField(max_length=12, choices=TICKET_TYPE, default='TASK')

    def __str__(self):
        return self.title


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
    submitted_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_on = models.DateTimeField(verbose_name="created on", auto_now_add=True)
    note = models.CharField(max_length=70)
    attachment = models.FileField()

    def __str__(self):
        return self.note


class Todo(models.Model):
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_on = models.DateTimeField(verbose_name="created on", auto_now_add=True)
    note = models.CharField(max_length=50)

    def __str__(self):
        return self.note


class DirectMessage(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    receiver = models.ForeignKey(Profile, related_name="direct_messages" , on_delete=models.CASCADE)
    created_on = models.DateTimeField(verbose_name="created on", auto_now_add=True)
    body = models.CharField(max_length=200)

    def __str__(self):
        return self.author
