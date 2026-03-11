"""
AI context for the Email Marketing module.
Loaded into the assistant system prompt when this module's tools are active.
"""

CONTEXT = """
## Module Knowledge: Email Marketing

### Models

**EmailTemplate**
- `name` (CharField) — internal template name
- `subject` (CharField) — email subject line
- `body_html` (TextField) — full HTML body of the email
- `is_active` (BooleanField, default True) — whether the template is available for use

**EmailCampaign**
- `name` (CharField) — campaign name
- `template` (FK → EmailTemplate, SET_NULL) — the email template used
- `status` (CharField, default 'draft') — typical values: draft, scheduled, sending, sent, cancelled
- `scheduled_at` (DateTimeField, nullable) — when the campaign is scheduled to send
- `sent_count` (PositiveIntegerField) — number of emails sent
- `open_count` (PositiveIntegerField) — number of opens tracked
- `click_count` (PositiveIntegerField) — number of link clicks tracked

### Key flows

1. **Template creation**: Create an EmailTemplate with name, subject, and HTML body. Mark `is_active=True`.
2. **Campaign setup**: Create EmailCampaign with a name and link a template. Set `status='draft'`.
3. **Schedule**: Set `scheduled_at` and change `status='scheduled'`.
4. **Track results**: Update `sent_count`, `open_count`, `click_count` as the campaign runs.

### Relationships
- EmailCampaign → EmailTemplate (FK, nullable)
- No direct FK to customers — recipient lists are managed externally or filtered at send time
- For richer multi-channel messaging (WhatsApp, SMS), use the `messaging` module instead
"""
