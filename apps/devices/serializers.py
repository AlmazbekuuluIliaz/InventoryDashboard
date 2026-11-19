from __future__ import annotations

from rest_framework import serializers

from apps.accounts.models import Organization
from apps.accounts.serializers import OrganizationSerializer
from apps.devices.models import Device, DeviceType


class DeviceTypeSerializer(serializers.ModelSerializer):
    """CRUD-сериализатор справочника типов устройств."""

    class Meta:
        model = DeviceType
        fields = ("id", "name", "slug", "description", "created_at")
        read_only_fields = ("id", "created_at")


class DeviceSerializer(serializers.ModelSerializer):
    """CRUD-сериализатор устройства.

    На чтение отдаёт вложенные тип и организацию, на запись принимает их id
    (``device_type_id`` / ``organization_id``). Поля ``status`` и ``last_seen``
    управляются системой и доступны только для чтения.
    """

    device_type = DeviceTypeSerializer(read_only=True)
    device_type_id = serializers.PrimaryKeyRelatedField(
        queryset=DeviceType.objects.all(),
        source="device_type",
        write_only=True,
    )
    organization = OrganizationSerializer(read_only=True)
    organization_id = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(),
        source="organization",
        write_only=True,
    )
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Device
        fields = (
            "id",
            "organization",
            "organization_id",
            "device_type",
            "device_type_id",
            "name",
            "serial_number",
            "status",
            "status_display",
            "last_seen",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "status",
            "last_seen",
            "created_at",
            "updated_at",
        )
