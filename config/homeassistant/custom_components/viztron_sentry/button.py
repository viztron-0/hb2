from homeassistant.components.button import ButtonEntity
from homeassistant.components import mqtt
from .const import MQTT_PREFIX
COMMANDS = "deploy return_to_base inquiry speak fire aim failsafe"
async def async_setup_entry(hass, entry, async_add):
    async_add([ViztronSentryButton(entry,c) for c in COMMANDS.split()])
class ViztronSentryButton(ButtonEntity):
    def __init__(self, entry, cmd):
        self._entry=entry; self._cmd=cmd
        self._attr_name=f"Sentry {cmd.replace('_',' ').title()}"
    async def async_press(self):
        await mqtt.async_publish(
            self.hass,f"{MQTT_PREFIX}/command/{self._cmd}","ON",0,False)
