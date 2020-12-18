from django.urls import path
from . import views


urlpatterns = [
    path('profile/', views.profile_view, name = "user_profile"),
    path('register/', views.register_view, name = "registration_page"),
    path('login/', views.login_view, name = "login_page"),
    path('logout/', views.logout_view, name = "logout"),
]
