from django.db import models
from UserApp.models import User
# Create your models here.

class OTP(models.Model):
    mail = models.EmailField(null=False, unique=True)
    otp = models.IntegerField()
    expiry = models.DateTimeField()
