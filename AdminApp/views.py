from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
import json
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from FileApp.models import Catogery
from UserApp.models import User

# Create your views here.
def response(obj, code=200):
    return JsonResponse(obj, status=code, safe=False)

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
    if user is not None and user.role == User.ADMIN:
        auth_login(request=request, user=user)
        return response({"success":"Login Sucess!"})
    else:
        return response({"error":"Invalid Username or Password!"}, 400)

def set_catogery_size(request: HttpRequest):
    if request.method != "POST":
        return response({"error":request.method + " NOT ALLOWED!"}, 405)
    print(request.user)
    if not request.user.is_authenticated or request.user.role != User.ADMIN:
        return response({"error":"AUTHENTICATION FAILED"}, 403)
    
    POST_DATA = json.loads(request.body)
    catogery = int(POST_DATA["category"])
    new_size = int(POST_DATA["size"])

    if new_size <= 0:
        return response({"error":"Invalid Size!"}, 400)

    if Catogery.objects.filter(id=catogery).exists():
        catogery = Catogery.objects.get(id=catogery)
        catogery.size = new_size
        catogery.save()
        return response({"success":"Catogery Size Updated Successfully!"})
    else:
        return response({"error":"Catogery does not exists!"}, 400)

def logout(request:HttpRequest):
    if request.user.is_authenticated and request.user.role == User.ADMIN:
        auth_logout(request)
        return response({"success":"Logout Sucessfull!"})
    else:
        return response({"error":"Unauthorised Access!"}, 401)
    