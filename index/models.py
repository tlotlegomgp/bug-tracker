from django.db import models
from account.models import Profile


# Create your models here.


class Todo(models.Model):

    TODO_STATUS = (
        ('COM', 'Completed'),
        ('SCH', 'Scheduled'),
    )

    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_on = models.DateTimeField(verbose_name="created on", auto_now_add=True)
    note = models.CharField(max_length=80)
    status = models.CharField(max_length=6, choices=TODO_STATUS, default='SCH')

    def __str__(self):
        return self.note


class Conversation(models.Model):
    user_1 =  models.ForeignKey(Profile, related_name="user_1", on_delete=models.CASCADE)
    user_2 =  models.ForeignKey(Profile, related_name="user_2", on_delete=models.CASCADE)
    slug = models.SlugField(unique= True, blank = True)

    def __str__(self):
        return self.user_1.user.username + " " + self.user_2.user.username



class DirectMessage(models.Model):

    MESSAGE_STATUS = (
        ('READ', 'Read'),
        ('UNREAD', 'Unread'),
    )

    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    receiver = models.ForeignKey(Profile, related_name="direct_messages", on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, blank=True, null=True)
    created_on = models.DateTimeField(verbose_name="created on", auto_now_add=True)
    body = models.CharField(max_length=500)
    status = models.CharField(max_length=6, choices=MESSAGE_STATUS, default='UNREAD')

    def __str__(self):
        return self.author.first_name + " " + self.author.last_name


class Alert(models.Model):

    ALERT_STATUS = (
        ('READ', 'Read'),
        ('UNREAD', 'Unread'),
    )

    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_on = models.DateTimeField(verbose_name="created on", auto_now_add=True)
    note = models.CharField(max_length=150)
    status = models.CharField(max_length=6, choices=ALERT_STATUS, default='UNREAD')
    url = models.URLField(blank=True)

    def __str__(self):
        return self.note
