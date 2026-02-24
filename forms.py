from django import forms
from django.utils.translation import gettext_lazy as _

from .models import EmailTemplate, EmailCampaign

class EmailTemplateForm(forms.ModelForm):
    class Meta:
        model = EmailTemplate
        fields = ['name', 'subject', 'body_html', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'subject': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'body_html': forms.Textarea(attrs={'class': 'textarea textarea-sm w-full', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'toggle'}),
        }

class EmailCampaignForm(forms.ModelForm):
    class Meta:
        model = EmailCampaign
        fields = ['name', 'template', 'status', 'scheduled_at', 'sent_count', 'open_count', 'click_count']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'template': forms.Select(attrs={'class': 'select select-sm w-full'}),
            'status': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'scheduled_at': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'datetime-local'}),
            'sent_count': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
            'open_count': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
            'click_count': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
        }

