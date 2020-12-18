from django.urls import path
from . import views


urlpatterns = [
    path('', views.tickets_view, name = "tickets_page"),
]