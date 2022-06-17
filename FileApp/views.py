from datetime import datetime
import json
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from hurry.filesize import size
from pytz import UTC
from FolderApp.models import Folder
from .models import Catogery, File, MiMeType
from hurry.filesize import size
from UserApp.models import User

# Create your views here.
def response(obj, code=200):
    return JsonResponse(obj, status=code, safe=False)

def upload(request: HttpRequest):
    if request.method != "POST":
        return response({"error":request.method+"NOT ALLOWED"}, 405)
    
    if not request.user.is_authenticated or request.user.role != User.USER:
        return response({"error":"AUTHENTICATION FAILED"}, 403)

    POST_DATA = request.POST
    folder = POST_DATA["folder"]
    file = request.FILES["file"]


    folder = Folder.objects.filter(id=folder)
    if folder.exists() and folder[0].user == request.user:
        
        if MiMeType.objects.filter(type=file.content_type).exists():
            catogery = MiMeType.objects.get(type=file.content_type).catogery
        else:
            catogery = Catogery.objects.get(name="others")
        if catogery.size < file.size:
            return response({"error":"MAX LIMIT EXCEEDED!"}, 400)
        File.objects.create(file=file, folder=folder[0], catogery=catogery, filename=file.name, size=size(file.size))
        folder[0].modified_at = datetime.now(tz=UTC)
        folder[0].save()
        return response({"success":"Upload Success"})
    else:
        return response({"error":"Invalid Folder!"}, 400)

def max_limit(request: HttpRequest):
    if request.method != "POST":
        return response({"error":request.method+"NOT ALLOWED"}, 405)
    
    if not request.user.is_authenticated:
        return response({"error":"AUTHENTICATION FAILED"}, 403)
    POST_DATA = json.loads(request.body)
    type = POST_DATA["type"]

    if MiMeType.objects.filter(type=type).exists():
            size = MiMeType.objects.get(type=type).catogery.size
    else:
            size = Catogery.objects.get(name="others").catogery.size
            
    return response({"max_limit":size})

def catogery_list(request: HttpRequest):
    if request.method != "GET":
        return response({"error":request.method+"NOT ALLOWED"}, 405)
    
    if not request.user.is_authenticated:
        return response({"error":"AUTHENTICATION FAILED"}, 403)

    catogeries = list(Catogery.objects.values())

    return response({"list": catogeries})
    