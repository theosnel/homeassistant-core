"""Generic XSense Entity Class."""
from __future__ import annotations

from homeassistant.const import CONF_EMAIL
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER
from .coordinator import XSenseDataUpdateCoordinator


class XSenseEntity(CoordinatorEntity[XSenseDataUpdateCoordinator]):
    """Represent a XSense Entity."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: XSenseDataUpdateCoordinator,
        device_id: str,
    ) -> None:
        """Initialise the gateway."""
        super().__init__(coordinator)
        self._dev_id = device_id

        device = coordinator.data[device_id]

        self.name = self.entity_description.key
        self._attr_unique_id = f"{device.device_id}-{self.entity_description.key}"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, device_id)},
            manufacturer=MANUFACTURER,
            model=device.device_type,
            name=device.name,
            via_device=(DOMAIN, coordinator.entry.data[CONF_EMAIL]),
        )

    # @property
    # def available(self) -> bool:
    #     """Return if entity is available."""
    #     return (
    #         self._dev_id in self.coordinator.data.devices
    #         and ("available" not in self.device or self.device["available"] is True)
    #         and super().available
    #     )

    async def async_added_to_hass(self) -> None:
        """Subscribe to updates."""
        self._handle_coordinator_update()
        await super().async_added_to_hass()
