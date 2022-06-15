from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from .models import User
from FolderApp.models import Folder
import re, json

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
# Create your views here.
def response(obj, code=200):
    return JsonResponse(obj, status=code, safe=False)

def register(POST_DATA):
    fname = POST_DATA["fname"]
    lname = POST_DATA["lname"]
    username = POST_DATA["username"]
    mail = POST_DATA["mail"]
    passw = POST_DATA["passw"]

    if fname == "" or User.objects.filter(username=username).exists() or re.search("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", passw) == None:
        return False
    
    user = User.objects.create_user(first_name=fname, last_name=lname, username=username, email=mail, password=passw)
    Folder.objects.create(user=user,name="$ROOT")
    return True

def username_available(request: HttpRequest):
    if request.method != "POST":
        return response({"error":request.method+" NOT ALLOWED!"}, 405)

    POST_DATA = json.loads(request.body)
    username = POST_DATA["username"]
    if User.objects.filter(username=username).exists():
        return response({"error":"Username NOT Available"}, 400)
 
    return response({"success":"Username Available"})

def login(request: HttpRequest):
    if request.method != "POST":
        return response({"error":request.method + " NOT ALLOWED!"}, 405)
    POST_DATA = json.loads(request.body)
    id = POST_DATA["id"]
    passw = POST_DATA["passw"]
    if User.objects.filter(email=id).exists():
        username = User.objects.get(email=id).username
    else:
        username = id
    user = authenticate(request=request, username=username, password=passw)
    if user is not None and user.role == User.USER:
        return response({"success":"Login Sucess!"})
    else:
        return response({"error":"Invalid Username or Password!"}, 400)