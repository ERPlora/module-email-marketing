from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import HubBaseModel

class EmailTemplate(HubBaseModel):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    subject = models.CharField(max_length=255, verbose_name=_('Subject'))
    body_html = models.TextField(blank=True, verbose_name=_('Body Html'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))

    class Meta(HubBaseModel.Meta):
        db_table = 'email_marketing_emailtemplate'

    def __str__(self):
        return self.name


class EmailCampaign(HubBaseModel):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    template = models.ForeignKey('EmailTemplate', on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, default='draft', verbose_name=_('Status'))
    scheduled_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Scheduled At'))
    sent_count = models.PositiveIntegerField(default=0, verbose_name=_('Sent Count'))
    open_count = models.PositiveIntegerField(default=0, verbose_name=_('Open Count'))
    click_count = models.PositiveIntegerField(default=0, verbose_name=_('Click Count'))

    class Meta(HubBaseModel.Meta):
        db_table = 'email_marketing_emailcampaign'

    def __str__(self):
        return self.name

