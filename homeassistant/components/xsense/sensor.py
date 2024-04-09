"""Support for xsense sensors."""
from __future__ import annotations

from xsense import device

from homeassistant import config_entries
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import CONF_EMAIL, SIGNAL_STRENGTH_DECIBELS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, MANUFACTURER


async def async_setup_entry(
    hass: HomeAssistant,
    entry: config_entries.ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the xsense sensor entry."""
    devices = []
    api = hass.data[DOMAIN][entry.entry_id]
    await api.load_all()
    for _, h in api.houses.items():
        for _, s in h.stations.items():
            await api.get_state(s)
            for _, d in s.devices.items():
                devices.append(XSenseSensor(d, entry))

    async_add_entities(devices)


class XSenseSensor(SensorEntity):
    """Representation of a xsense device."""

    _attr_native_unit_of_measurement = SIGNAL_STRENGTH_DECIBELS
    _attr_device_class = SensorDeviceClass.SIGNAL_STRENGTH
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, dev: device, entry) -> None:
        """Initiate xsense device."""
        self._attr_unique_id = dev.sn
        self._attr_name = dev.name
        self._attr_native_value = dev.rf_level

        self._attr_device_info: DeviceInfo = DeviceInfo(
            name=dev.name,
            manufacturer=MANUFACTURER,
            model=dev.device_type,
            identifiers={(DOMAIN, dev.sn)},
            via_device=(DOMAIN, entry.data[CONF_EMAIL]),
        )
