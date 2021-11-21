from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager



class User(AbstractUser):
    objects = UserManager()



class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='img/profiles/', blank=True, null=True)



    def __str__(self):
        return str(self.user)
