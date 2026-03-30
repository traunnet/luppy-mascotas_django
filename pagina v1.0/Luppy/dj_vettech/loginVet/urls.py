from django.urls import path  
from django.contrib.auth import views as auth_views
from . import views

app_name = 'auth_app' # Puedes ponerle el nombre que quieras
urlpatterns = [
    path('', views.login_view, name='login'), 
    path('registro/', views.registro, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]