from __future__ import annotations

from django.db import models

from apps.devices.models import Device


class TelemetryLog(models.Model):
    """Сырое событие телеметрии от устройства с произвольным payload."""

    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name="telemetry_logs",
        verbose_name="Устройство",
    )
    payload = models.JSONField("Данные", default=dict, blank=True)
    created_at = models.DateTimeField("Получено", auto_now_add=True)

    class Meta:
        verbose_name = "Запись телеметрии"
        verbose_name_plural = "Журнал телеметрии"
        ordering = ("-created_at",)
        indexes = [
            models.Index(
                fields=("device", "-created_at"),
                name="telemetry_device_ts_idx",
            ),
            models.Index(
                fields=("-created_at",),
                name="telemetry_created_idx",
            ),
        ]

    def __str__(self) -> str:
        return f"#{self.pk} · device={self.device_id}"
