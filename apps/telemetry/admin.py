from __future__ import annotations

from django.contrib import admin

from apps.telemetry.models import TelemetryLog


@admin.register(TelemetryLog)
class TelemetryLogAdmin(admin.ModelAdmin):
    list_display = ("id", "device", "created_at")
    list_filter = ("device__organization", "device__device_type", "created_at")
    search_fields = ("device__name", "device__serial_number")
    list_select_related = ("device", "device__organization")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
