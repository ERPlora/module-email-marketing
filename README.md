# Email Marketing Module

Email campaigns, templates and automation.

## Features

- Create and manage email campaigns with scheduling
- Design reusable email templates with HTML body content
- Track campaign performance: sent count, open count, click count
- Campaign lifecycle management with status tracking (draft, scheduled, sent, etc.)
- Link campaigns to email templates
- Schedule campaigns for future delivery
- Dashboard overview of campaign metrics and performance
- Activate or deactivate email templates

## Installation

This module is installed automatically via the ERPlora Marketplace.

## Configuration

Access settings via: **Menu > Email Marketing > Settings**

## Usage

Access via: **Menu > Email Marketing**

### Views

| View | URL | Description |
|------|-----|-------------|
| Dashboard | `/m/email_marketing/dashboard/` | Overview of campaign performance and metrics |
| Campaigns | `/m/email_marketing/campaigns/` | Create, schedule and manage email campaigns |
| Templates | `/m/email_marketing/templates/` | Design and manage reusable email templates |
| Settings | `/m/email_marketing/settings/` | Module configuration |

## Models

| Model | Description |
|-------|-------------|
| `EmailTemplate` | A reusable email template with name, subject line, HTML body, and active flag |
| `EmailCampaign` | An email campaign linked to a template, with status, scheduled send time, and engagement metrics (sent, open, click counts) |

## Permissions

| Permission | Description |
|------------|-------------|
| `email_marketing.view_emailcampaign` | View email campaigns |
| `email_marketing.add_emailcampaign` | Create new email campaigns |
| `email_marketing.change_emailcampaign` | Edit existing email campaigns |
| `email_marketing.delete_emailcampaign` | Delete email campaigns |
| `email_marketing.view_emailtemplate` | View email templates |
| `email_marketing.add_emailtemplate` | Create new email templates |
| `email_marketing.change_emailtemplate` | Edit existing email templates |
| `email_marketing.manage_settings` | Manage module settings |

## License

MIT

## Author

ERPlora Team - support@erplora.com
