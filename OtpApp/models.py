from django.db import models
from UserApp.models import User
# Create your models here.

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.IntegerField()
    expiry = models.DateTimeField()
