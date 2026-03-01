"""AI tools for the Email Marketing module."""
from assistant.tools import AssistantTool, register_tool


@register_tool
class ListEmailTemplates(AssistantTool):
    name = "list_email_templates"
    description = "List email marketing templates."
    module_id = "email_marketing"
    required_permission = "email_marketing.view_emailtemplate"
    parameters = {"type": "object", "properties": {"is_active": {"type": "boolean"}}, "required": [], "additionalProperties": False}

    def execute(self, args, request):
        from email_marketing.models import EmailTemplate
        qs = EmailTemplate.objects.all()
        if 'is_active' in args:
            qs = qs.filter(is_active=args['is_active'])
        return {"templates": [{"id": str(t.id), "name": t.name, "subject": t.subject, "is_active": t.is_active} for t in qs]}


@register_tool
class CreateEmailTemplate(AssistantTool):
    name = "create_email_template"
    description = "Create an email marketing template."
    module_id = "email_marketing"
    required_permission = "email_marketing.add_emailtemplate"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {"name": {"type": "string"}, "subject": {"type": "string"}, "body_html": {"type": "string"}},
        "required": ["name", "subject", "body_html"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from email_marketing.models import EmailTemplate
        t = EmailTemplate.objects.create(name=args['name'], subject=args['subject'], body_html=args['body_html'])
        return {"id": str(t.id), "name": t.name, "created": True}


@register_tool
class ListEmailCampaigns(AssistantTool):
    name = "list_email_campaigns"
    description = "List email campaigns."
    module_id = "email_marketing"
    required_permission = "email_marketing.view_emailcampaign"
    parameters = {"type": "object", "properties": {"status": {"type": "string"}}, "required": [], "additionalProperties": False}

    def execute(self, args, request):
        from email_marketing.models import EmailCampaign
        qs = EmailCampaign.objects.select_related('template').all()
        if args.get('status'):
            qs = qs.filter(status=args['status'])
        return {"campaigns": [{"id": str(c.id), "name": c.name, "template": c.template.name if c.template else None, "status": c.status, "sent_count": c.sent_count, "open_count": c.open_count, "click_count": c.click_count} for c in qs]}
