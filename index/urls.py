from django.urls import path
from . import views


urlpatterns = [
    path('', views.index_view, name="index_page"),
    path('add-todo/', views.add_todo_view, name="add_todo"),
    path('delete-todo/<int:id>', views.delete_todo_view, name="delete_todo"),
]
