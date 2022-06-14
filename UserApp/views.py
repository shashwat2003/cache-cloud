from django.shortcuts import render
from .models import User
import re
# Create your views here.
def register(POST_DATA):
    fname = POST_DATA["fname"]
    lname = POST_DATA["lname"]
    username = POST_DATA["username"]
    mail = POST_DATA["mail"]
    passw = POST_DATA["passw"]

    if fname == "" or User.objects.filter(username=username).exists() or re.search("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", passw) == None:
        return False
    
    User.objects.create_user(first_name=fname, last_name=lname, username=username, email=mail, password=passw)
    return True
