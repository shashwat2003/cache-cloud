from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    USER = 1
    ADMIN = 2
    ROLE_CHOICES = ((USER,"User"), (ADMIN,"Admin"))
    
    username = models.CharField(max_length=15, unique=True, null=False)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=1)
