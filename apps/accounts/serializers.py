from __future__ import annotations

from rest_framework import serializers

from apps.accounts.models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    """Компактное представление организации для вложенного отображения."""

    class Meta:
        model = Organization
        fields = ("id", "name", "slug", "is_active")
        read_only_fields = fields
