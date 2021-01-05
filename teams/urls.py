from django.urls import path
from . import views


urlpatterns = [
    path('', views.team_view, name="team_page"),
    path('management/', views.user_management_view, name="user_management"),
    path('<slug:slug>/', views.update_user_view, name="update_user"),
    path('send-message/<int:user_id>/', views.send_message_view, name="send_message"),
]
