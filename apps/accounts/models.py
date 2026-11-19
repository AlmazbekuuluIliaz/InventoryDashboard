from __future__ import annotations

from django.db import models


class Organization(models.Model):
    """Тенант платформы: владелец устройств и телеметрии."""

    name = models.CharField("Название", max_length=255, unique=True)
    slug = models.SlugField("Слаг", max_length=255, unique=True)
    is_active = models.BooleanField("Активна", default=True)
    created_at = models.DateTimeField("Создана", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлена", auto_now=True)

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name
