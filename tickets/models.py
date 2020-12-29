import random
import string
import os
from django.shortcuts import get_object_or_404
from django.db import models
from index.models import Alert
from account.models import Profile
from projects.models import Project
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from django.dispatch import receiver


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

    ROLE = (
        ('SUB', 'Submitter'),
        ('DEV', 'Developer'),
    )

    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user_role = models.CharField(max_length=20, choices=ROLE, default='DEV')
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


def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))


def pre_save_ticket_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title + "-" + rand_slug())


def ticket_post_save_receiver(sender, instance, *args, **kwargs):
    action_user = instance.ticket.created_by.first_name + " " + instance.ticket.created_by.last_name
    alert_user = instance.user
    project_name = instance.ticket.project.name
    alert_message = action_user + " assigned you to a ticket in project, " + project_name + "."

    if instance.ticket.created_by != instance.user:
        alert = Alert.objects.create(user=alert_user, note=alert_message)


def ticket_comment_post_save_receiver(sender, instance, *args, **kwargs):
    ticket_assignment = get_object_or_404(TicketAssignee, ticket=instance.ticket)
    action_user = ticket_assignment.user.first_name + " " + ticket_assignment.user.last_name
    alert_user = instance.user
    ticket_name = instance.ticket.title
    alert_message = action_user + " added a comment to ticket, " + ticket_name + "."

    if instance.ticket.created_by != instance.user:
        alert = Alert.objects.create(user=alert_user, note=alert_message)


def ticket_attachment_post_save_receiver(sender, instance, *args, **kwargs):
    ticket_assignment = get_object_or_404(TicketAssignee, ticket=instance.ticket)
    action_user = ticket_assignment.user.first_name + " " + ticket_assignment.user.last_name
    alert_user = instance.user
    ticket_name = instance.ticket.title
    alert_message = action_user + " added a attachment to ticket, " + ticket_name + "."

    if instance.ticket.created_by != instance.user:
        alert = Alert.objects.create(user=alert_user, note=alert_message)


pre_save.connect(pre_save_ticket_receiver, sender=Ticket)
post_save.connect(ticket_post_save_receiver, sender=TicketAssignee)
post_save.connect(ticket_comment_post_save_receiver, sender=TicketComment)
post_save.connect(ticket_attachment_post_save_receiver, sender=TicketAttachment)
