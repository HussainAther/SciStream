"""Public and API routes for the focused research-session demo."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/execute/", views.execute_code, name="execute_code"),
    path("api/assistant/", views.assistant, name="assistant"),
    path("api/summary/", views.generate_summary, name="generate_summary"),
]
