from __future__ import annotations

import django_filters as filters

from apps.devices.models import Device, DeviceType


class DeviceFilter(filters.FilterSet):
    """Фильтрация устройств по организации, типу, статусу и ``last_seen``.

    Примеры:
        ``?organization=1``
        ``?type=3`` (id типа устройства)
        ``?status=active``
        ``?last_seen_after=2026-01-01T00:00:00Z``
        ``?last_seen_before=2026-02-01T00:00:00Z``
        ``?seen=true`` (устройства, которые хоть раз выходили на связь)
    """

    type = filters.ModelChoiceFilter(
        field_name="device_type",
        queryset=DeviceType.objects.all(),
        label="Тип устройства",
    )
    last_seen_after = filters.IsoDateTimeFilter(
        field_name="last_seen",
        lookup_expr="gte",
        label="last_seen не раньше",
    )
    last_seen_before = filters.IsoDateTimeFilter(
        field_name="last_seen",
        lookup_expr="lte",
        label="last_seen не позже",
    )
    seen = filters.BooleanFilter(
        field_name="last_seen",
        lookup_expr="isnull",
        exclude=True,
        label="Выходило на связь",
    )

    class Meta:
        model = Device
        fields = {
            "organization": ["exact"],
            "status": ["exact"],
        }
