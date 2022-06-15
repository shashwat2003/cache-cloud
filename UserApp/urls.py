from django.urls import path
from .views import *

urlpatterns = [
    path("login/", login),
    path("username_check/", username_available),
]
