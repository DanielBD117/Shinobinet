"""
URL configuration for djangocrud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tareas import views
from django.contrib.auth import views as auth_views
from django.contrib.sites.shortcuts import get_current_site

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('inscripcion/', views.inscripcion, name='inscripcion'),
    path('tareas/', views.tareas, name='tareas'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='login'),
    path('tareas/crear_tareas/', views.crear_tareas, name='crear_tareas'),
    path('tareas/<int:task_id>/', views.detalle_tarea, name='detalles_tareas'),
    path('tareas/<int:task_id>/completar/', views.completar, name='completar'),
    path('tareas/<int:task_id>/eliminar/', views.eliminar, name='eliminar'),
    path('tareas_completadas/', views.tareas_completadas, name= 'tareas_completadas'),

    #Recuperacion de cuentas
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html',email_template_name='registration/password_reset_email.html',subject_template_name='registration/password_reset_subject.txt',from_email='FitLife 💪 <tu_correo@gmail.com>',extra_email_context={'domain': 'fitlife.com','protocol': 'https'}), name='reset_password'),
    path('reset_password_done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]



