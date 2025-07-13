from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.core import callback
async def async_setup_entry(hass, entry, async_add):
    async_add([ViztronSentryConnected(entry)])
class ViztronSentryConnected(BinarySensorEntity):
    _attr_name = "Sentry Connected"
    def __init__(self, entry): self._entry=entry; self._state=False
    async def async_added_to_hass(self):
        self.async_on_remove(async_dispatcher_connect(
            self.hass,"viztron_sentry_update",self._update))
    @callback
    def _update(self,payload):
        if "connection" in payload:
            self._state=payload["connection"]; self.async_write_ha_state()
    @property
    def is_on(self): return self._state
