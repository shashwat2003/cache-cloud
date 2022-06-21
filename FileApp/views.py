from datetime import datetime, timedelta
import json
from django.http import FileResponse, HttpRequest, JsonResponse
from django.shortcuts import render
from pytz import UTC
from FolderApp.models import Folder
from .models import Catogery, File, MiMeType
from UserApp.models import User
from django.conf import settings
import os

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
        File.objects.create(file=file, folder=folder[0], catogery=catogery, filename=file.name, size=file.size)
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

def download(request: HttpRequest):
    if request.method != "POST":
        return response({"error":request.method + " NOT ALLOWED"}, 405)
    # if not request.user.is_authenticated:
    #     return response({"error":"AUTHENTICATION FAILED"}, 403)

    POST_DATA = json.loads(request.body)
    file_id = int(POST_DATA["id"])
    
    if File.objects.filter(id=file_id).exists():
        file = File.objects.get(id=file_id)
        if file.folder.user != request.user:
            return response({"error":"Not Allowed"}, 403)
        path = os.path.join(settings.MEDIA_ROOT, file.file.url)
        # with open(path, "rb") as f:
        f = open(path, "rb")
        return FileResponse(f, as_attachment=True, filename=file.filename)

def delete(request: HttpRequest):
    if request.method != "POST":
        return response({"error":request.method+"NOT ALLOWED"}, 405)
    
    if not request.user.is_authenticated or request.user.role != User.USER:
        return response({"error":"AUTHENTICATION FAILED"}, 403)

    POST_DATA = json.loads(request.body)
    file = int(POST_DATA["file"])
    file = File.objects.filter(id=file, deleted=False).first()

    if file is not None and file.folder.user == request.user:
        file.deleted = 1
        file.expiry = datetime.now(tz=UTC) + timedelta(days=30)
        file.save()
        return response({"success":"File has been moved to Trash!"})
    else:
        return response({"error":"Wrong File Selected!"}, 400)

def restore(request: HttpRequest):
    if request.method != "POST":
        return response({"error":request.method+"NOT ALLOWED"}, 405)
    
    if not request.user.is_authenticated or request.user.role != User.USER:
        return response({"error":"AUTHENTICATION FAILED"}, 403)

    POST_DATA = json.loads(request.body)
    file = int(POST_DATA["file"])
    file = File.objects.filter(id=file, deleted=True).first()

    if file is not None and file.folder.user == request.user and file.expiry > datetime.now(tz=UTC):
        if file.folder.deleted:
            return response({"error":"Parent Folder has been deleted!"}, 400)
        file.deleted = 0
        file.expiry = None
        file.save()
        return response({"success":"File has been restored!"})
    else:
        return response({"error":"Wrong File Selected!"}, 400)


    