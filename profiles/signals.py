from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Relationship

@receiver(post_save, sender=User)
# signal receivers must accept keyword (**kwargs) parameter
def create_profile(instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=Relationship)
def add_remove_friend(instance, created, **kwargs):
    sender_profile = instance.sender
    receiver_profile = instance.receiver

    if instance.status == 'accept':
        sender_profile.friends.add(receiver_profile)
        receiver_profile.friends.add(sender_profile)
    elif instance.status == 'remove':
        sender_profile.friends.remove(receiver_profile)
        receiver_profile.friends.remove(sender_profile)

    sender_profile.save()
    receiver_profile.save()