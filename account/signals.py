import random
import string
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_save
from index.models import Alert
from .models import Profile


def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))


def pre_save_profile_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.user.email + "-" + rand_slug())


def post_save_profile_receiver(sender, instance, created, **kwargs):
    if created:
        alert_user = instance
        alert_message = "Welcome to Liquid!"

        alert = Alert.objects.create(user=alert_user, note=alert_message)


pre_save.connect(pre_save_profile_receiver, sender=Profile)
post_save.connect(post_save_profile_receiver, sender=Profile)
