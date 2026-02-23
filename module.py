from django.utils.translation import gettext_lazy as _

MODULE_ID = 'email_marketing'
MODULE_NAME = _('Email Marketing')
MODULE_VERSION = '1.0.0'
MODULE_ICON = 'mail-outline'
MODULE_DESCRIPTION = _('Email campaigns, templates and automation')
MODULE_AUTHOR = 'ERPlora'
MODULE_CATEGORY = 'marketing'

MENU = {
    'label': _('Email Marketing'),
    'icon': 'mail-outline',
    'order': 53,
}

NAVIGATION = [
    {'label': _('Dashboard'), 'icon': 'speedometer-outline', 'id': 'dashboard'},
{'label': _('Campaigns'), 'icon': 'mail-outline', 'id': 'campaigns'},
{'label': _('Templates'), 'icon': 'document-outline', 'id': 'templates'},
{'label': _('Settings'), 'icon': 'settings-outline', 'id': 'settings'},
]

DEPENDENCIES = []

PERMISSIONS = [
    'email_marketing.view_emailcampaign',
'email_marketing.add_emailcampaign',
'email_marketing.change_emailcampaign',
'email_marketing.delete_emailcampaign',
'email_marketing.view_emailtemplate',
'email_marketing.add_emailtemplate',
'email_marketing.change_emailtemplate',
'email_marketing.manage_settings',
]
