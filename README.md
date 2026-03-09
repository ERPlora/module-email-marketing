# Email Marketing

## Overview

| Property | Value |
|----------|-------|
| **Module ID** | `email_marketing` |
| **Version** | `1.0.0` |
| **Icon** | `mail-outline` |
| **Dependencies** | None |

## Models

### `EmailTemplate`

EmailTemplate(id, hub_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, name, subject, body_html, is_active)

| Field | Type | Details |
|-------|------|---------|
| `name` | CharField | max_length=255 |
| `subject` | CharField | max_length=255 |
| `body_html` | TextField | optional |
| `is_active` | BooleanField |  |

### `EmailCampaign`

EmailCampaign(id, hub_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, name, template, status, scheduled_at, sent_count, open_count, click_count)

| Field | Type | Details |
|-------|------|---------|
| `name` | CharField | max_length=255 |
| `template` | ForeignKey | → `email_marketing.EmailTemplate`, on_delete=SET_NULL, optional |
| `status` | CharField | max_length=20 |
| `scheduled_at` | DateTimeField | optional |
| `sent_count` | PositiveIntegerField |  |
| `open_count` | PositiveIntegerField |  |
| `click_count` | PositiveIntegerField |  |

## Cross-Module Relationships

| From | Field | To | on_delete | Nullable |
|------|-------|----|-----------|----------|
| `EmailCampaign` | `template` | `email_marketing.EmailTemplate` | SET_NULL | Yes |

## URL Endpoints

Base path: `/m/email_marketing/`

| Path | Name | Method |
|------|------|--------|
| `(root)` | `dashboard` | GET |
| `campaigns/` | `campaigns` | GET |
| `templates/` | `templates` | GET |
| `email_templates/` | `email_templates_list` | GET |
| `email_templates/add/` | `email_template_add` | GET/POST |
| `email_templates/<uuid:pk>/edit/` | `email_template_edit` | GET |
| `email_templates/<uuid:pk>/delete/` | `email_template_delete` | GET/POST |
| `email_templates/<uuid:pk>/toggle/` | `email_template_toggle_status` | GET |
| `email_templates/bulk/` | `email_templates_bulk_action` | GET/POST |
| `email_campaigns/` | `email_campaigns_list` | GET |
| `email_campaigns/add/` | `email_campaign_add` | GET/POST |
| `email_campaigns/<uuid:pk>/edit/` | `email_campaign_edit` | GET |
| `email_campaigns/<uuid:pk>/delete/` | `email_campaign_delete` | GET/POST |
| `email_campaigns/bulk/` | `email_campaigns_bulk_action` | GET/POST |
| `settings/` | `settings` | GET |

## Permissions

| Permission | Description |
|------------|-------------|
| `email_marketing.view_emailcampaign` | View Emailcampaign |
| `email_marketing.add_emailcampaign` | Add Emailcampaign |
| `email_marketing.change_emailcampaign` | Change Emailcampaign |
| `email_marketing.delete_emailcampaign` | Delete Emailcampaign |
| `email_marketing.view_emailtemplate` | View Emailtemplate |
| `email_marketing.add_emailtemplate` | Add Emailtemplate |
| `email_marketing.change_emailtemplate` | Change Emailtemplate |
| `email_marketing.manage_settings` | Manage Settings |

**Role assignments:**

- **admin**: All permissions
- **manager**: `add_emailcampaign`, `add_emailtemplate`, `change_emailcampaign`, `change_emailtemplate`, `view_emailcampaign`, `view_emailtemplate`
- **employee**: `add_emailcampaign`, `view_emailcampaign`, `view_emailtemplate`

## Navigation

| View | Icon | ID | Fullpage |
|------|------|----|----------|
| Dashboard | `speedometer-outline` | `dashboard` | No |
| Campaigns | `mail-outline` | `campaigns` | No |
| Templates | `document-outline` | `templates` | No |
| Settings | `settings-outline` | `settings` | No |

## AI Tools

Tools available for the AI assistant:

### `list_email_templates`

List email marketing templates.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `is_active` | boolean | No |  |

### `create_email_template`

Create an email marketing template.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes |  |
| `subject` | string | Yes |  |
| `body_html` | string | Yes |  |

### `list_email_campaigns`

List email campaigns.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `status` | string | No |  |

## File Structure

```
README.md
__init__.py
admin.py
ai_tools.py
apps.py
forms.py
locale/
  en/
    LC_MESSAGES/
      django.po
  es/
    LC_MESSAGES/
      django.po
migrations/
  0001_initial.py
  __init__.py
models.py
module.py
static/
  email_marketing/
    css/
    js/
  icons/
    icon.svg
templates/
  email_marketing/
    pages/
      campaigns.html
      dashboard.html
      email_campaign_add.html
      email_campaign_edit.html
      email_campaigns.html
      email_template_add.html
      email_template_edit.html
      email_templates.html
      index.html
      settings.html
      templates.html
    partials/
      campaigns_content.html
      dashboard_content.html
      email_campaign_add_content.html
      email_campaign_edit_content.html
      email_campaigns_content.html
      email_campaigns_list.html
      email_template_add_content.html
      email_template_edit_content.html
      email_templates_content.html
      email_templates_list.html
      panel_email_campaign_add.html
      panel_email_campaign_edit.html
      panel_email_template_add.html
      panel_email_template_edit.html
      settings_content.html
      templates_content.html
tests/
  __init__.py
  conftest.py
  test_models.py
  test_views.py
urls.py
views.py
```
