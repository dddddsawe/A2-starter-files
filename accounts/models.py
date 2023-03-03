from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Add any additional fields you want to the User model here
    bio = models.CharField(max_length=255)
