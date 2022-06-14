from django.http import HttpRequest, JsonResponse
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

def generate(request: HttpRequest):
    # send_mail(subject="Testing", message="Hello!", from_email=settings.EMAIL_HOST_USER, recipient_list=["shashwat13.8@gmail.com",])
    return JsonResponse({"success":"Sent!"})