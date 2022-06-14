from django.urls import path
from .views import *

urlpatterns = [
    path("generate/", generate),
    path("verify/", verify)
]
