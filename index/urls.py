from django.urls import path
from . import views


urlpatterns = [
    path('', views.index_view, name = "index_page"),
    path('team/', views.team_view, name = "team_page"),
    path('projects/', views.projects_view, name = "projects_page")
]
