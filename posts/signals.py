from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from .models import Post

import random


def post_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


pre_save.connect(post_pre_save, sender=Post)

def post_pre_save_update(sender, instance, *args, **kwargs):
    if instance.slug:
        instance.slug = slugify(instance.title)


pre_save.connect(post_pre_save_update, sender=Post)


