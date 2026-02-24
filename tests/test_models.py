"""Tests for email_marketing models."""
import pytest
from django.utils import timezone

from email_marketing.models import EmailTemplate, EmailCampaign


@pytest.mark.django_db
class TestEmailTemplate:
    """EmailTemplate model tests."""

    def test_create(self, email_template):
        """Test EmailTemplate creation."""
        assert email_template.pk is not None
        assert email_template.is_deleted is False

    def test_str(self, email_template):
        """Test string representation."""
        assert str(email_template) is not None
        assert len(str(email_template)) > 0

    def test_soft_delete(self, email_template):
        """Test soft delete."""
        pk = email_template.pk
        email_template.is_deleted = True
        email_template.deleted_at = timezone.now()
        email_template.save()
        assert not EmailTemplate.objects.filter(pk=pk).exists()
        assert EmailTemplate.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, email_template):
        """Test default queryset excludes deleted."""
        email_template.is_deleted = True
        email_template.deleted_at = timezone.now()
        email_template.save()
        assert EmailTemplate.objects.filter(hub_id=hub_id).count() == 0

    def test_toggle_active(self, email_template):
        """Test toggling is_active."""
        original = email_template.is_active
        email_template.is_active = not original
        email_template.save()
        email_template.refresh_from_db()
        assert email_template.is_active != original


@pytest.mark.django_db
class TestEmailCampaign:
    """EmailCampaign model tests."""

    def test_create(self, email_campaign):
        """Test EmailCampaign creation."""
        assert email_campaign.pk is not None
        assert email_campaign.is_deleted is False

    def test_str(self, email_campaign):
        """Test string representation."""
        assert str(email_campaign) is not None
        assert len(str(email_campaign)) > 0

    def test_soft_delete(self, email_campaign):
        """Test soft delete."""
        pk = email_campaign.pk
        email_campaign.is_deleted = True
        email_campaign.deleted_at = timezone.now()
        email_campaign.save()
        assert not EmailCampaign.objects.filter(pk=pk).exists()
        assert EmailCampaign.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, email_campaign):
        """Test default queryset excludes deleted."""
        email_campaign.is_deleted = True
        email_campaign.deleted_at = timezone.now()
        email_campaign.save()
        assert EmailCampaign.objects.filter(hub_id=hub_id).count() == 0


