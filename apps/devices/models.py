from __future__ import annotations

from django.db import models

from apps.accounts.models import Organization


class DeviceType(models.Model):
    """Справочник типов устройств (модель/класс оборудования)."""

    name = models.CharField("Название", max_length=255, unique=True)
    slug = models.SlugField("Слаг", max_length=255, unique=True)
    description = models.TextField("Описание", blank=True)
    created_at = models.DateTimeField("Создан", auto_now_add=True)

    class Meta:
        verbose_name = "Тип устройства"
        verbose_name_plural = "Типы устройств"
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Device(models.Model):
    """Единица оборудования, принадлежащая организации."""

    class Status(models.TextChoices):
        ACTIVE = "active", "Активно"
        INACTIVE = "inactive", "Неактивно"
        MAINTENANCE = "maintenance", "Обслуживание"
        DECOMMISSIONED = "decommissioned", "Выведено из эксплуатации"

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="devices",
        verbose_name="Организация",
    )
    device_type = models.ForeignKey(
        DeviceType,
        on_delete=models.PROTECT,
        related_name="devices",
        verbose_name="Тип устройства",
    )
    name = models.CharField("Название", max_length=255)
    serial_number = models.CharField("Серийный номер", max_length=255, blank=True)
    status = models.CharField(
        "Статус",
        max_length=32,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    last_seen = models.DateTimeField("Последняя активность", null=True, blank=True)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        verbose_name = "Устройство"
        verbose_name_plural = "Устройства"
        ordering = ("name",)
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "serial_number"),
                condition=~models.Q(serial_number=""),
                name="uniq_device_serial_per_org",
            ),
        ]
        indexes = [
            models.Index(
                fields=("organization", "status"),
                name="device_org_status_idx",
            ),
            models.Index(
                fields=("status", "last_seen"),
                name="device_status_seen_idx",
            ),
            models.Index(
                fields=("last_seen",),
                name="device_last_seen_idx",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.get_status_display()})"
