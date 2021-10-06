from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    pass



class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    def __str__(self):
        return self.user.email
