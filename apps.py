from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EmailMarketingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'email_marketing'
    label = 'email_marketing'
    verbose_name = _('Email Marketing')

    def ready(self):
        pass
