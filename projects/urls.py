from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects_view, name = "projects_page"),
]
