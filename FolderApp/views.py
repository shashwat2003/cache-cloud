from datetime import datetime, timedelta
import json
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from pytz import UTC

from FileApp.views import delete
from .models import Folder
from FileApp.models import File
from django.db.models import Count
from UserApp.models import User
from hurry.filesize import size
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

    if Folder.objects.filter(id=parent, deleted=False).exists() and Folder.objects.get(id=parent).user == request.user:
        parent = Folder.objects.get(id=parent)
        if Folder.objects.filter(user=request.user, parent=parent, name=name).exists():
            return response({"error":"Folder With same name already exists in the directory!"}, 400)
        Folder.objects.create(user=request.user, name=name, parent=parent)
        parent.modified_at = datetime.now(tz=UTC)
        parent.save()
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

    folder = Folder.objects.filter(id=folder, deleted=False)
    if folder.exists() and folder[0].user == request.user:
        # print(size(file.size))
        folder = folder[0]
        if folder.name != "$ROOT":
            folders = [{"name":"...","id":folder.parent.id}] + list(Folder.objects.filter(user=request.user, parent=folder, deleted=False).annotate(files=Count('file')).values())
            folderName = folder.name
            
        else:
            folders = list(Folder.objects.filter(user=request.user, parent=folder, deleted=False).annotate(files=Count('file')).values())
            folderName = "Home"

        # files = list(File.objects.filter(folder=folder).annotate(size_format=size(Value('size'))).values())
        files = []
        for i in File.objects.filter(folder=folder, deleted=False).values():
            i["size"] = size(i["size"])
            files.append(i)
        return response({"folders":folders, "files":files, "folderId": folder.id, "folderName":folderName})
        
    else:
        return response({"error":"Invalid Folder!"}, 400)

def delete(request: HttpRequest):
    if request.method != "POST":
        return response({"error":request.method+"NOT ALLOWED"}, 405)
    
    if not request.user.is_authenticated or request.user.role != User.USER:
        return response({"error":"AUTHENTICATION FAILED"}, 403)

    POST_DATA = json.loads(request.body)
    folder = int(POST_DATA["folder"])
    folder = Folder.objects.filter(id=folder, deleted=False).first()

    if folder is not None and folder.user == request.user:
        if File.objects.filter(folder=folder, deleted=False).exists() or Folder.objects.filter(parent=folder, deleted=False).exists():
            return response({"error":"Directory is not Empty!"}, 400)
        folder.deleted = 1
        folder.expiry = datetime.now(tz=UTC) + timedelta(days=30)
        folder.save()
        return response({"success":"Folder has been moved to Trash!"})
    else:
        return response({"error":"Wrong File Selected!"}, 400)

def restore(request: HttpRequest):
    if request.method != "POST":
        return response({"error":request.method+"NOT ALLOWED"}, 405)
    
    if not request.user.is_authenticated or request.user.role != User.USER:
        return response({"error":"AUTHENTICATION FAILED"}, 403)

    POST_DATA = json.loads(request.body)
    folder = int(POST_DATA["folder"])
    folder = Folder.objects.filter(id=folder, deleted=True).first()

    if folder is not None and folder.user == request.user and folder.expiry > datetime.now(tz=UTC):
        if folder.parent.deleted:
            return response({"error":"Parent Folder has been deleted!"}, 400)
        folder.deleted = 0
        folder.expiry = None
        folder.save()
        return response({"success":"Folder has been restored!"})
    else:
        return response({"error":"Wrong Folder Selected!"}, 400)
