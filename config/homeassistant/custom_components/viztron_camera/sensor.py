from __future__ import annotations
from homeassistant.helpers.entity import Entity
from homeassistant.core import callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
SENSOR_TYPES = {
    "tracked_objects": ("Tracked Objects","objects"),
    "threat_score_max": ("Max Threat Score","score")
}
async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([ViztronCameraSensor(entry,k) for k in SENSOR_TYPES])
class ViztronCameraSensor(Entity):
    def __init__(self, entry, key):
        self._entry = entry; self._key = key
        self._attr_name = f"Camera {SENSOR_TYPES[key][0]}"
        self._state = None
    async def async_added_to_hass(self):
        self.async_on_remove(async_dispatcher_connect(
            self.hass,"viztron_camera_update",self._update))
    @callback
    def _update(self,payload):
        if self._key in payload:
            self._state = payload[self._key]; self.async_write_ha_state()
    @property
    def state(self): return self._state
