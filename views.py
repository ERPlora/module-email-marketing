"""
Email Marketing Module Views
"""
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from apps.accounts.decorators import login_required
from apps.core.htmx import htmx_view
from apps.modules_runtime.navigation import with_module_nav


@login_required
@with_module_nav('email_marketing', 'dashboard')
@htmx_view('email_marketing/pages/dashboard.html', 'email_marketing/partials/dashboard_content.html')
def dashboard(request):
    """Dashboard view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('email_marketing', 'campaigns')
@htmx_view('email_marketing/pages/campaigns.html', 'email_marketing/partials/campaigns_content.html')
def campaigns(request):
    """Campaigns view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('email_marketing', 'templates')
@htmx_view('email_marketing/pages/templates.html', 'email_marketing/partials/templates_content.html')
def templates(request):
    """Templates view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('email_marketing', 'settings')
@htmx_view('email_marketing/pages/settings.html', 'email_marketing/partials/settings_content.html')
def settings(request):
    """Settings view."""
    hub_id = request.session.get('hub_id')
    return {}

