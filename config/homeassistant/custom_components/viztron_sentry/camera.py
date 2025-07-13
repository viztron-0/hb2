from homeassistant.components.camera import Camera
from .const import DOMAIN
class ViztronSentryCamera(Camera):
    def __init__(self, entry):
        super().__init__(); self._entry=entry; self._url=None
        self._attr_name="Sentry Stream"
    async def async_added_to_hass(self):
        self.hass.helpers.dispatcher.async_dispatcher_connect(
            self.hass,"viztron_sentry_update",self._update)
    async def stream_source(self): return self._url
    def _update(self,payload):
        url=payload.get("stream_url")
        if url: self._url=url; self.async_write_ha_state()
