from __future__ import annotations

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from apps.devices.filters import DeviceFilter
from apps.devices.models import Device, DeviceType
from apps.devices.serializers import DeviceSerializer, DeviceTypeSerializer


class DeviceTypeViewSet(viewsets.ModelViewSet):
    """CRUD по справочнику типов устройств."""

    queryset = DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("name", "slug")
    ordering_fields = ("name", "created_at")


class DeviceViewSet(viewsets.ModelViewSet):
    """CRUD по устройствам.

    Queryset использует ``select_related`` по FK (организация, тип), чтобы
    листинг и detail не плодили лишних запросов.
    """

    queryset = Device.objects.select_related("organization", "device_type")
    serializer_class = DeviceSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_class = DeviceFilter
    search_fields = ("name", "serial_number")
    ordering_fields = ("name", "status", "last_seen", "created_at")
    ordering = ("name",)
