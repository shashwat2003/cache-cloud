from django.urls import path
from .views import *

urlpatterns = [
    path("upload/", upload),
    path("max_limit/", max_limit),
    path("catogery_list/", catogery_list),
]
