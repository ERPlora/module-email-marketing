"""Tests for email_marketing views."""
import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestDashboard:
    """Dashboard view tests."""

    def test_dashboard_loads(self, auth_client):
        """Test dashboard page loads."""
        url = reverse('email_marketing:dashboard')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_dashboard_htmx(self, auth_client):
        """Test dashboard HTMX partial."""
        url = reverse('email_marketing:dashboard')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_dashboard_requires_auth(self, client):
        """Test dashboard requires authentication."""
        url = reverse('email_marketing:dashboard')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestEmailTemplateViews:
    """EmailTemplate view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('email_marketing:email_templates_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('email_marketing:email_templates_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('email_marketing:email_templates_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('email_marketing:email_templates_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('email_marketing:email_templates_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('email_marketing:email_templates_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('email_marketing:email_template_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('email_marketing:email_template_add')
        data = {
            'name': 'New Name',
            'subject': 'New Subject',
            'body_html': 'Test description',
            'is_active': 'on',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, email_template):
        """Test edit form loads."""
        url = reverse('email_marketing:email_template_edit', args=[email_template.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, email_template):
        """Test editing via POST."""
        url = reverse('email_marketing:email_template_edit', args=[email_template.pk])
        data = {
            'name': 'Updated Name',
            'subject': 'Updated Subject',
            'body_html': 'Test description',
            'is_active': '',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, email_template):
        """Test soft delete via POST."""
        url = reverse('email_marketing:email_template_delete', args=[email_template.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        email_template.refresh_from_db()
        assert email_template.is_deleted is True

    def test_toggle_status(self, auth_client, email_template):
        """Test toggle active status."""
        url = reverse('email_marketing:email_template_toggle_status', args=[email_template.pk])
        original = email_template.is_active
        response = auth_client.post(url)
        assert response.status_code == 200
        email_template.refresh_from_db()
        assert email_template.is_active != original

    def test_bulk_delete(self, auth_client, email_template):
        """Test bulk delete."""
        url = reverse('email_marketing:email_templates_bulk_action')
        response = auth_client.post(url, {'ids': str(email_template.pk), 'action': 'delete'})
        assert response.status_code == 200
        email_template.refresh_from_db()
        assert email_template.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('email_marketing:email_templates_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestEmailCampaignViews:
    """EmailCampaign view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('email_marketing:email_campaigns_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('email_marketing:email_campaigns_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('email_marketing:email_campaigns_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('email_marketing:email_campaigns_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('email_marketing:email_campaigns_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('email_marketing:email_campaigns_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('email_marketing:email_campaign_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('email_marketing:email_campaign_add')
        data = {
            'name': 'New Name',
            'status': 'New Status',
            'scheduled_at': '2025-01-15T10:00',
            'sent_count': '5',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, email_campaign):
        """Test edit form loads."""
        url = reverse('email_marketing:email_campaign_edit', args=[email_campaign.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, email_campaign):
        """Test editing via POST."""
        url = reverse('email_marketing:email_campaign_edit', args=[email_campaign.pk])
        data = {
            'name': 'Updated Name',
            'status': 'Updated Status',
            'scheduled_at': '2025-01-15T10:00',
            'sent_count': '5',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, email_campaign):
        """Test soft delete via POST."""
        url = reverse('email_marketing:email_campaign_delete', args=[email_campaign.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        email_campaign.refresh_from_db()
        assert email_campaign.is_deleted is True

    def test_bulk_delete(self, auth_client, email_campaign):
        """Test bulk delete."""
        url = reverse('email_marketing:email_campaigns_bulk_action')
        response = auth_client.post(url, {'ids': str(email_campaign.pk), 'action': 'delete'})
        assert response.status_code == 200
        email_campaign.refresh_from_db()
        assert email_campaign.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('email_marketing:email_campaigns_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestSettings:
    """Settings view tests."""

    def test_settings_loads(self, auth_client):
        """Test settings page loads."""
        url = reverse('email_marketing:settings')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_settings_requires_auth(self, client):
        """Test settings requires authentication."""
        url = reverse('email_marketing:settings')
        response = client.get(url)
        assert response.status_code == 302

