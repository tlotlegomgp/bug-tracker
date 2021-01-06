from django.urls import path
from . import views


urlpatterns = [
    path('', views.index_view, name="index_page"),
    path('add-todo/', views.add_todo_view, name="add_todo"),
    path('delete-todo/<int:id>', views.delete_todo_view, name="delete_todo"),
    path('clear-alerts/', views.clear_alerts_view, name="clear_alerts"),
    path('clear-messages/', views.clear_messages_view, name="clear_messages"),
    path('conversation/<slug:slug>/<int:message_id>/', views.conversation_view, name="view_conversation"),
]
