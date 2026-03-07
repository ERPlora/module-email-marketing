"""
Email Marketing Module Views
"""
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, render as django_render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from apps.accounts.decorators import login_required, permission_required
from apps.core.htmx import htmx_view
from apps.core.services import export_to_csv, export_to_excel
from apps.modules_runtime.navigation import with_module_nav

from .models import EmailTemplate, EmailCampaign

PER_PAGE_CHOICES = [10, 25, 50, 100]


# ======================================================================
# Dashboard
# ======================================================================

@login_required
@with_module_nav('email_marketing', 'dashboard')
@htmx_view('email_marketing/pages/index.html', 'email_marketing/partials/dashboard_content.html')
def dashboard(request):
    hub_id = request.session.get('hub_id')
    return {
        'total_email_templates': EmailTemplate.objects.filter(hub_id=hub_id, is_deleted=False).count(),
        'total_email_campaigns': EmailCampaign.objects.filter(hub_id=hub_id, is_deleted=False).count(),
    }


# ======================================================================
# EmailTemplate
# ======================================================================

EMAIL_TEMPLATE_SORT_FIELDS = {
    'subject': 'subject',
    'name': 'name',
    'is_active': 'is_active',
    'body_html': 'body_html',
    'created_at': 'created_at',
}

def _build_email_templates_context(hub_id, per_page=10):
    qs = EmailTemplate.objects.filter(hub_id=hub_id, is_deleted=False).order_by('subject')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'email_templates': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'subject',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_email_templates_list(request, hub_id, per_page=10):
    ctx = _build_email_templates_context(hub_id, per_page)
    return django_render(request, 'email_marketing/partials/email_templates_list.html', ctx)

@login_required
@with_module_nav('email_marketing', 'campaigns')
@htmx_view('email_marketing/pages/email_templates.html', 'email_marketing/partials/email_templates_content.html')
def email_templates_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'subject')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = EmailTemplate.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(name__icontains=search_query) | Q(subject__icontains=search_query) | Q(body_html__icontains=search_query))

    order_by = EMAIL_TEMPLATE_SORT_FIELDS.get(sort_field, 'subject')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['subject', 'name', 'is_active', 'body_html']
        headers = ['Subject', 'Name', 'Is Active', 'Body Html']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='email_templates.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='email_templates.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'email_marketing/partials/email_templates_list.html', {
            'email_templates': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'email_templates': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
@htmx_view('email_marketing/pages/email_template_add.html', 'email_marketing/partials/email_template_add_content.html')
def email_template_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        subject = request.POST.get('subject', '').strip()
        body_html = request.POST.get('body_html', '').strip()
        is_active = request.POST.get('is_active') == 'on'
        obj = EmailTemplate(hub_id=hub_id)
        obj.name = name
        obj.subject = subject
        obj.body_html = body_html
        obj.is_active = is_active
        obj.save()
        response = HttpResponse(status=204)
        response['HX-Redirect'] = reverse('email_marketing:email_templates_list')
        return response
    return {}

@login_required
@htmx_view('email_marketing/pages/email_template_edit.html', 'email_marketing/partials/email_template_edit_content.html')
def email_template_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(EmailTemplate, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '').strip()
        obj.subject = request.POST.get('subject', '').strip()
        obj.body_html = request.POST.get('body_html', '').strip()
        obj.is_active = request.POST.get('is_active') == 'on'
        obj.save()
        return _render_email_templates_list(request, hub_id)
    return {'obj': obj}

@login_required
@require_POST
def email_template_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(EmailTemplate, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_email_templates_list(request, hub_id)

@login_required
@require_POST
def email_template_toggle_status(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(EmailTemplate, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_active = not obj.is_active
    obj.save(update_fields=['is_active', 'updated_at'])
    return _render_email_templates_list(request, hub_id)

@login_required
@require_POST
def email_templates_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = EmailTemplate.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'activate':
        qs.update(is_active=True)
    elif action == 'deactivate':
        qs.update(is_active=False)
    elif action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_email_templates_list(request, hub_id)


# ======================================================================
# EmailCampaign
# ======================================================================

EMAIL_CAMPAIGN_SORT_FIELDS = {
    'name': 'name',
    'template': 'template',
    'status': 'status',
    'click_count': 'click_count',
    'open_count': 'open_count',
    'sent_count': 'sent_count',
    'created_at': 'created_at',
}

def _build_email_campaigns_context(hub_id, per_page=10):
    qs = EmailCampaign.objects.filter(hub_id=hub_id, is_deleted=False).order_by('name')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'email_campaigns': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'name',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_email_campaigns_list(request, hub_id, per_page=10):
    ctx = _build_email_campaigns_context(hub_id, per_page)
    return django_render(request, 'email_marketing/partials/email_campaigns_list.html', ctx)

@login_required
@with_module_nav('email_marketing', 'campaigns')
@htmx_view('email_marketing/pages/email_campaigns.html', 'email_marketing/partials/email_campaigns_content.html')
def email_campaigns_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'name')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = EmailCampaign.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(name__icontains=search_query) | Q(status__icontains=search_query))

    order_by = EMAIL_CAMPAIGN_SORT_FIELDS.get(sort_field, 'name')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['name', 'template', 'status', 'click_count', 'open_count', 'sent_count']
        headers = ['Name', 'EmailTemplate', 'Status', 'Click Count', 'Open Count', 'Sent Count']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='email_campaigns.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='email_campaigns.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'email_marketing/partials/email_campaigns_list.html', {
            'email_campaigns': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'email_campaigns': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
@htmx_view('email_marketing/pages/email_campaign_add.html', 'email_marketing/partials/email_campaign_add_content.html')
def email_campaign_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        status = request.POST.get('status', '').strip()
        scheduled_at = request.POST.get('scheduled_at') or None
        sent_count = int(request.POST.get('sent_count', 0) or 0)
        open_count = int(request.POST.get('open_count', 0) or 0)
        click_count = int(request.POST.get('click_count', 0) or 0)
        obj = EmailCampaign(hub_id=hub_id)
        obj.name = name
        obj.status = status
        obj.scheduled_at = scheduled_at
        obj.sent_count = sent_count
        obj.open_count = open_count
        obj.click_count = click_count
        obj.save()
        response = HttpResponse(status=204)
        response['HX-Redirect'] = reverse('email_marketing:email_campaigns_list')
        return response
    return {}

@login_required
@htmx_view('email_marketing/pages/email_campaign_edit.html', 'email_marketing/partials/email_campaign_edit_content.html')
def email_campaign_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(EmailCampaign, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '').strip()
        obj.status = request.POST.get('status', '').strip()
        obj.scheduled_at = request.POST.get('scheduled_at') or None
        obj.sent_count = int(request.POST.get('sent_count', 0) or 0)
        obj.open_count = int(request.POST.get('open_count', 0) or 0)
        obj.click_count = int(request.POST.get('click_count', 0) or 0)
        obj.save()
        return _render_email_campaigns_list(request, hub_id)
    return {'obj': obj}

@login_required
@require_POST
def email_campaign_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(EmailCampaign, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_email_campaigns_list(request, hub_id)

@login_required
@require_POST
def email_campaigns_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = EmailCampaign.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_email_campaigns_list(request, hub_id)


@login_required
@permission_required('email_marketing.manage_settings')
@with_module_nav('email_marketing', 'settings')
@htmx_view('email_marketing/pages/settings.html', 'email_marketing/partials/settings_content.html')
def settings_view(request):
    return {}

