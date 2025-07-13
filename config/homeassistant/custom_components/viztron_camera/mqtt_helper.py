from __future__ import annotations
import asyncio, json, logging
from homeassistant.core import HomeAssistant, callback
from homeassistant.components import mqtt
from .const import MQTT_PREFIX
_LOGGER = logging.getLogger(__name__)
class ViztronMQTT:
    def __init__(self, hass: HomeAssistant):
        self._hass = hass
        self._tasks: list[asyncio.Task] = []
    async def async_subscribe(self):
        topic = f"{MQTT_PREFIX}/status/#"
        _LOGGER.debug("Subscribing to %s", topic)
        await mqtt.async_subscribe(self._hass, topic, self._msg, 0)
    @callback
    def _msg(self, msg):
        try:
            payload = json.loads(msg.payload)
        except ValueError:
            _LOGGER.warning("Bad JSON on %s", msg.topic); return
        self._hass.helpers.dispatcher.async_dispatcher_send(
            f"viztron_camera_update", payload)
    async def async_disconnect(self):
        for t in self._tasks:
            t.cancel()
