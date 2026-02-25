from django.urls import path
from . import views

app_name = 'email_marketing'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Navigation tab aliases
    path('campaigns/', views.email_templates_list, name='campaigns'),
    path('templates/', views.dashboard, name='templates'),


    # EmailTemplate
    path('email_templates/', views.email_templates_list, name='email_templates_list'),
    path('email_templates/add/', views.email_template_add, name='email_template_add'),
    path('email_templates/<uuid:pk>/edit/', views.email_template_edit, name='email_template_edit'),
    path('email_templates/<uuid:pk>/delete/', views.email_template_delete, name='email_template_delete'),
    path('email_templates/<uuid:pk>/toggle/', views.email_template_toggle_status, name='email_template_toggle_status'),
    path('email_templates/bulk/', views.email_templates_bulk_action, name='email_templates_bulk_action'),

    # EmailCampaign
    path('email_campaigns/', views.email_campaigns_list, name='email_campaigns_list'),
    path('email_campaigns/add/', views.email_campaign_add, name='email_campaign_add'),
    path('email_campaigns/<uuid:pk>/edit/', views.email_campaign_edit, name='email_campaign_edit'),
    path('email_campaigns/<uuid:pk>/delete/', views.email_campaign_delete, name='email_campaign_delete'),
    path('email_campaigns/bulk/', views.email_campaigns_bulk_action, name='email_campaigns_bulk_action'),

    # Settings
    path('settings/', views.settings_view, name='settings'),
]
