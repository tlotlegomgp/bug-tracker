from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('profile/', views.profile_view, name="user_profile"),
    path('profile/<slug:slug>/', views.profile_detail_view, name="view_profile"),
    path('register/', views.register_view, name="registration_page"),
    path('login/', views.login_view, name="login_page"),
    path('logout/', views.logout_view, name="logout"),
    path('demo/', views.demo_view, name="demo_account"),
    path('demo-login/<slug:role>', views.demo_login_view, name="demo_login"),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='account/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='account/password_change_done.html'), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='account/password_reset.html',
                                                                 email_template_name='account/password_reset_email.html', subject_template_name='account/password_reset_subject.txt'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'), name='password_reset_complete'),
]
