from datetime import datetime
import json
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from pytz import UTC
from .models import Folder
from FileApp.models import File
from django.db.models import Count
from UserApp.models import User
# Create your views here.
def response(obj, code=200):
    return JsonResponse(obj, status=code, safe=False)

def create(request: HttpRequest):
    if request.method != "POST":
        return response({"error":request.method+" NOT ALLOWED!"}, 405)

    if not request.user.is_authenticated or request.user.role != User.USER:
        return response({"error":"AUTHENTICATION FAILURE!"}, 403)

    POST_DATA = json.loads(request.body)
    name = POST_DATA["name"]
    parent = POST_DATA["parent"]

    if Folder.objects.filter(id=parent).exists() and Folder.objects.get(id=parent).user == request.user:
        parent = Folder.objects.get(id=parent)
        Folder.objects.create(user=request.user, name=name, parent=parent)
        parent.modified_at = datetime.now(tz=UTC)
        return response({"success":"Folder Created!"},201)

    else:
        return response({"error":"Invalid Folder Selected!"},403)

def get_data(request: HttpRequest):
    if request.method != "POST":
        return response({"error":request.method+"NOT ALLOWED"}, 405)

    if not request.user.is_authenticated or request.user.role != User.USER:
        return response({"error":"AUTHENTICATION FAILED"}, 403)
    POST_DATA = json.loads(request.body)
    folder = POST_DATA["folder"]

    folder = Folder.objects.filter(id=folder)
    if folder.exists() and folder[0].user == request.user:
        # print(size(file.size))
        folder = folder[0]
        if folder.name != "$ROOT":
            folders = [{"name":"...","id":folder.parent.id}] + list(Folder.objects.filter(user=request.user, parent=folder).annotate(files=Count('file')).values())
            folderName = folder.name
            
        else:
            folders = list(Folder.objects.filter(user=request.user, parent=folder).annotate(files=Count('file')).values())
            folderName = "Home"
        files = list(File.objects.filter(folder=folder).values())
        return response({"folders":folders, "files":files, "folderId": folder.id, "folderName":folderName})
        
    else:
        return response({"error":"Invalid Folder!"}, 400)

    
