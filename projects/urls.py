from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects_view, name="projects_page"),
    path('add-project/', views.add_project_view, name="add_project"),
    path('project/<slug:slug>/', views.project_detail_view, name="view_project"),
]
