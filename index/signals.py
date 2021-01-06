import random
import string
from django.db.models.signals import pre_save
from django.utils.text import slugify
from .models import Conversation


def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))


def pre_save_conversation_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(rand_slug() + "-" + rand_slug())


pre_save.connect(pre_save_conversation_receiver, sender=Conversation)
