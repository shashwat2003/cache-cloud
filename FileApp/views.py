import json
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from hurry.filesize import size
from FolderApp.models import Folder
from .models import File

# Create your views here.
def response(obj, code=200):
    return JsonResponse(obj, status=code, safe=False)

def upload(request: HttpRequest):
    if request.method != "POST":
        return response({"error":request.method+"NOT ALLOWED"}, 405)
    
    if not request.user.is_authenticated:
        return response({"error":"AUTHENTICATION FAILED"}, 403)

    POST_DATA =request.POST
    folder = POST_DATA["folder"]
    file = request.FILES["file"]
    if Folder.objects.filter(id=folder).exists() and Folder.objects.get(id=folder).user == request.user:
        print(size(file.size))
        # File.objects.create(file=file, folder=Folder.objects.get(id=folder))
        return response({"success":"Upload Success"})
    else:
        return response({"error":"Invalid Folder!"}, 400)

