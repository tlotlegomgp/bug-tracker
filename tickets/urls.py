from django.urls import path
from . import views


urlpatterns = [
    path('', views.tickets_view, name="tickets_page"),
    path('add-ticket/<slug:slug>/', views.add_ticket_view, name="add_ticket"),
    path('edit-ticket/<slug:slug>/', views.edit_ticket_view, name="edit_ticket"),

]
