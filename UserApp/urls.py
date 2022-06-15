from django.urls import path
from .views import *

urlpatterns = [
    path("login/", login),
    path("dashboard/", dashboard),
    path("username_check/", username_available),
]
