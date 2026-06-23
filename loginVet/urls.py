from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .forms import CustomPasswordResetForm
from . import views

app_name = 'auth_app'

urlpatterns = [
    path('', views.login_view, name='login'),
    path('registro/', views.registro, name='registro'),
    path('logout/', views.logout_view, name='logout'),

    # 1. Formulario de solicitud
path('password-reset/', 
     auth_views.PasswordResetView.as_view(
         form_class=CustomPasswordResetForm,
         template_name='registration/password_reset_form.html',
         email_template_name='registration/password_reset_email.txt', 
         html_email_template_name='registration/password_reset_email.html',
         subject_template_name='registration/password_reset_subject.txt',
         success_url=reverse_lazy('auth_app:password_reset_done')
     ), name='password_reset'),

    # 2. Confirmación de envío
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_finalizado.html'
         ), name='password_reset_done'),

    # 3. Formulario de nueva contraseña
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html',
             success_url=reverse_lazy('auth_app:password_reset_complete')
         ), name='password_reset_confirm'),

    # 4. Éxito final
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/finalizado_luppy.html'
         ), name='password_reset_complete'),
]