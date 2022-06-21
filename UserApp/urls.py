from django.urls import path
from .views import *

urlpatterns = [
    path("login/", login),
    path("logout/", logout),
    path("dashboard/", dashboard),
    path("trash/", trash),
    path("username_check/", username_available),
]
