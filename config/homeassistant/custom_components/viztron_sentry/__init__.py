\"\"\"Viztron sentry integration.\"\"\"
from __future__ import annotations
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from .const import DOMAIN
_LOGGER = logging.getLogger(__name__)
async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    return True
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {}
    from .mqtt_helper import ViztronMQTT
    client = ViztronMQTT(hass)
    await client.async_subscribe()
    hass.data[DOMAIN][entry.entry_id]["mqtt"] = client
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor","camera","binary_sensor","button"])
    return True
async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    await hass.config_entries.async_unload_platforms(entry, ["sensor","camera","binary_sensor","button"])
    await hass.data[DOMAIN][entry.entry_id]["mqtt"].async_disconnect()
    hass.data[DOMAIN].pop(entry.entry_id)
    return True
