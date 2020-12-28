from django.urls import path
from . import views


urlpatterns = [
    path('', views.tickets_view, name="tickets_page"),
    path('add/<slug:slug>/', views.add_ticket_view, name="add_ticket"),
    path('edit/<slug:slug>/', views.edit_ticket_view, name="edit_ticket"),
    path('delete/<slug:slug>/', views.delete_ticket_view, name="delete_ticket"),
    path('<slug:slug>/', views.ticket_detail_view, name="view_ticket"),
    path('add-attachment/<slug:slug>/', views.ticket_attachment_view, name="add_attachment"),
    path('delete-attachment/<int:attachment_id>/', views.delete_attachment_view, name="delete_attachment"),

]
