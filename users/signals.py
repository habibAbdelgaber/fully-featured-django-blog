from django.db.models.signals import post_save
from .models import Profile, User
from django.dispatch import receiver

# @receiver(post_save, sender=User)
# def post_save_user(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

def post_save_user(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(post_save_user, sender=User)