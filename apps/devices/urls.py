from __future__ import annotations

from rest_framework.routers import DefaultRouter

from apps.devices.views import DeviceTypeViewSet, DeviceViewSet

router = DefaultRouter()
router.register("devices", DeviceViewSet, basename="device")
router.register("device-types", DeviceTypeViewSet, basename="device-type")

urlpatterns = router.urls
