import random
import string
from django.shortcuts import get_object_or_404
from index.models import Alert
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from .models import Ticket, TicketAssignee, TicketAttachment, TicketComment


def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))


def pre_save_ticket_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title + "-" + rand_slug())


def ticket_post_save_receiver(sender, instance, created, **kwargs):
    if created:
        action_user = instance.ticket.created_by.first_name + " " + instance.ticket.created_by.last_name
        alert_user = instance.user
        project_name = instance.ticket.project.name
        alert_message = action_user + " assigned you to a ticket in project, " + project_name + "."
        alert_url = f'tickets/{instance.ticket.slug}/'

        if instance.ticket.created_by != instance.user:
            alert = Alert.objects.create(user=alert_user, note=alert_message, url = alert_url)


def ticket_comment_post_save_receiver(sender, instance, *args, **kwargs):
    ticket_assignment = get_object_or_404(TicketAssignee, ticket=instance.ticket)
    action_user = instance.user.first_name + " " + instance.user.last_name
    alert_user = ticket_assignment.user
    ticket_name = instance.ticket.title
    alert_message = action_user + " left a comment to ticket, " + ticket_name + "."

    if ticket_assignment.user != instance.user:
        alert = Alert.objects.create(user=alert_user, note=alert_message)


def ticket_attachment_post_save_receiver(sender, instance, *args, **kwargs):
    ticket_assignment = get_object_or_404(TicketAssignee, ticket=instance.ticket)
    action_user = instance.user.first_name + " " + instance.user.last_name
    alert_user = ticket_assignment.user
    ticket_name = instance.ticket.title
    alert_message = action_user + " added an attachment to ticket, " + ticket_name + "."

    if ticket_assignment.user != instance.user:
        alert = Alert.objects.create(user=alert_user, note=alert_message)


pre_save.connect(pre_save_ticket_receiver, sender=Ticket)
post_save.connect(ticket_post_save_receiver, sender=TicketAssignee)
post_save.connect(ticket_comment_post_save_receiver, sender=TicketComment)
post_save.connect(ticket_attachment_post_save_receiver, sender=TicketAttachment)
