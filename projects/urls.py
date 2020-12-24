from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects_view, name="projects_page"),
    path('add-project/', views.add_project_view, name="add_project"),
    path('edit/<slug:slug>/', views.edit_project_view, name="edit_project"),
    path('<slug:slug>/', views.project_detail_view, name="view_project"),
    path('delete/<slug:slug>/', views.delete_project_view, name="delete_project"),
]
