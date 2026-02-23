from django.urls import path
from . import views

app_name = 'email_marketing'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('campaigns/', views.campaigns, name='campaigns'),
    path('templates/', views.templates, name='templates'),
    path('settings/', views.settings, name='settings'),
]
