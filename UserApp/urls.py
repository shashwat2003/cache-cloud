from django.urls import path
from .views import *

urlpatterns = [
    path("username_check/", username_available),
]
