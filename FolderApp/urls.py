from django.urls import path
from .views import *

urlpatterns = [
    path("create/", create),
    path("get_data/", get_data),
    path("delete/", delete),
    path("restore/", restore),
]
