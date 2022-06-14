import json, random
from django.http import HttpRequest, JsonResponse
from django.core.mail import send_mail
from django.conf import settings

from .models import OTP
from UserApp.views import register
from UserApp.models import User

from datetime import datetime, timedelta
# Create your views here.

def response(obj, code=200):
    return JsonResponse(obj, status=code, safe=False)

def generate(request: HttpRequest):
    if request.method != "POST":
        return response({"error":request.method+" NOT ALLOWED!"}, 405)
    POST_DATA = json.loads(request.body)
    mail = POST_DATA["mail"]
    greet = POST_DATA["greet"]
    if User.objects.filter(email=mail).exists():
        return response({"error":"Mail Already Registered!"}, 403)
    if OTP.objects.filter(mail=mail).exists():
        OTP.objects.get(mail=mail).delete()
    otp = random.randint(1000, 9999)
    subject = "[OTP] Your E-Mail Verification OTP for CacheCloud"
    message = '''
Hi ''' + greet +''',

Welcome to CacheCloud! You are just a few steps away from creating your account!

Your E-Mail Verification OTP for CacheCloud is *''' + str(otp) + '''* !
The OTP is valid for 10 minutes only.

Regards,
Team CacheCloud

-------------------------------------------
WARNING: This is an auto-generated mail! Please DO-NOT reply to this mail. 
-------------------------------------------

    '''
    if(not send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=[mail])):
        return response({"error":"Problem sending mail!"}, 500)
    else:
        expiry = datetime.now() + timedelta(minutes=10)
        OTP.objects.create(mail=mail, otp=otp, expiry=expiry)
        return JsonResponse({"success":"OTP sent successfully!"})

def verify(request: HttpRequest):
    if request.method != "POST":
        return response({"error":request.method+" NOT ALLOWED!"}, 405)
        
    POST_DATA = json.loads(request.body)
    mail = POST_DATA["mail"]
    otp = int(POST_DATA["otp"])

    if OTP.objects.filter(mail=mail).exists():
        if OTP.objects.filter(mail=mail, expiry__gt=datetime.now()):
            if OTP.objects.get(mail=mail).otp == otp:                    
                if register(POST_DATA):
                    OTP.objects.get(mail=mail).delete()
                    return response({"success": "OTP Verified and Account Created!"}, 201)
                else:
                    return response({"error":"Invalid Request!"}, 403)
        else:
            OTP.objects.get(mail=mail).delete()

    return response({"error":"OTP Validation Failed"}, 403)
