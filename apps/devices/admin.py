from __future__ import annotations

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from apps.devices.models import Device, DeviceType


@admin.register(DeviceType)
class DeviceTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "organization",
        "device_type",
        "status",
        "last_seen",
        "created_at",
    )
    list_filter = ("status", "device_type", "organization")
    search_fields = ("name", "serial_number")
    list_select_related = ("organization", "device_type")
    autocomplete_fields = ("organization", "device_type")
    date_hierarchy = "created_at"
    ordering = ("name",)
    actions = ("mark_inactive", "mark_active")

    @admin.action(description="Пометить выбранные как неактивные")
    def mark_inactive(
        self, request: HttpRequest, queryset: QuerySet[Device]
    ) -> None:
        updated = queryset.update(status=Device.Status.INACTIVE)
        self.message_user(request, f"Помечено неактивными: {updated}")

    @admin.action(description="Пометить выбранные как активные")
    def mark_active(
        self, request: HttpRequest, queryset: QuerySet[Device]
    ) -> None:
        updated = queryset.update(status=Device.Status.ACTIVE)
        self.message_user(request, f"Помечено активными: {updated}")
