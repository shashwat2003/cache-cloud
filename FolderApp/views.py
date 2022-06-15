import json
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from .models import Folder
# Create your views here.
def response(obj, code=200):
    return JsonResponse(obj, status=code, safe=False)

def create(request: HttpRequest):
    if request.method != "POST":
        return response({"error":request.method+" NOT ALLOWED!"}, 405)

    if not request.user.is_authenticated:
        return response({"error":"AUTHENTICATION FAILURE!"}, 403)

    POST_DATA = json.loads(request.body)
    name = POST_DATA["name"]
    parent = POST_DATA["parent"]

    if Folder.objects.filter(id=parent).exists() and Folder.objects.get(id=parent).user == request.user:
        Folder.objects.create(user=request.user, name=name, parent=Folder.objects.get(id=parent))
        return response({"success":"Folder Created!"},201)

    else:
        return response({"error":"Invalid Folder Selected!"},403)
