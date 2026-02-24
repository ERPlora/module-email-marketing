from django.contrib import admin

from .models import EmailTemplate, EmailCampaign

@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'is_active', 'created_at']
    search_fields = ['name', 'subject', 'body_html']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(EmailCampaign)
class EmailCampaignAdmin(admin.ModelAdmin):
    list_display = ['name', 'template', 'status', 'scheduled_at', 'sent_count', 'created_at']
    search_fields = ['name', 'status']
    readonly_fields = ['created_at', 'updated_at']

