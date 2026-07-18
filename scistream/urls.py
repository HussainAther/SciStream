# scistream/urls.py
from django.urls import path
from streams.views import index

urlpatterns = [
    path("", index, name="index"),
]

