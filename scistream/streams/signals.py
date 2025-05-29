from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import StreamKey

@receiver(post_save, sender=User)
def create_stream_key(sender, instance, created, **kwargs):
    if created:
        StreamKey.objects.create(user=instance)

