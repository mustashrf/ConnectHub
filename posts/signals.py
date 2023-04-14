from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Like

@receiver(post_save, sender=Like)
def update_likes(instance, created, **kwargs):
    if created:
        instance.post.save()