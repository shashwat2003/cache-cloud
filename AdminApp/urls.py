from django.urls import path
from .views import *

urlpatterns = [
    path("login/", login),
    path("set_size/", set_catogery_size),
]
