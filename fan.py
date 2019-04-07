import logging
import voluptuous as vol
from homeassistant.components.fan import (FanEntity,
                                          SPEED_OFF,
                                          SPEED_LOW,
                                          SPEED_MEDIUM,
                                          SPEED_HIGH,
                                          SUPPORT_SET_SPEED,
                                          PLATFORM_SCHEMA)
from homeassistant.const import CONF_HOST
import homeassistant.helpers.config_validation as cv

DOMAIN = "quietcool"

REQUIREMENTS = [
    'https://github.com/stabbylambda/quietcool-python/archive/wip.zip#quietcool==1.0.0']

_LOGGER = logging.getLogger(__name__)

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string
})


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    import quietcool
    host = config.get(CONF_HOST)
    _LOGGER.info(f"Calling get fans for hub: {host}")
    hub = await quietcool.Hub.create(host)
    fans = await hub.get_fans()
    async_add_entities(QuietcoolFan(fan) for fan in fans)


class QuietcoolFan(FanEntity):
    def __init__(self, fan) -> None:
        self._fan = fan

    @property
    def supported_features(self) -> int:
        """Flag supported features."""
        return SUPPORT_SET_SPEED

    @property
    def is_on(self):
        return self._fan.current_power

    @property
    def speed_list(self) -> list:
        _LOGGER.info(f"{self.name} has {self._fan.configured_speeds} speeds")
        speeds = {
            1: [SPEED_OFF, SPEED_HIGH],
            2: [SPEED_OFF, SPEED_LOW, SPEED_HIGH],
            3: [SPEED_OFF, SPEED_LOW, SPEED_MEDIUM, SPEED_HIGH]
        }

        return speeds[self._fan.configured_speeds]

    @property
    def speed(self) -> str:
        """Return the current speed."""
        speed_map = {
            3: SPEED_HIGH,
            2: SPEED_MEDIUM,
            1: SPEED_LOW,
            0: SPEED_OFF
        }
        return speed_map[self._fan.current_speed]

    async def async_turn_on(self, speed: str = None, **kwargs) -> None:
        """Turn on the entity."""
        _LOGGER.info(f"Turning on {self.name}")
        await self._fan.turn_on()

    async def async_turn_off(self, **kwargs) -> None:
        """Turn on the entity."""
        _LOGGER.info(f"Turning off {self.name}")
        await self._fan.turn_off()

    async def async_set_speed(self, speed: str) -> None:
        """Set the speed of the fan."""
        _LOGGER.info(f"Setting {self.name} to {speed}")
        speed_map = {
            SPEED_HIGH: 3,
            SPEED_MEDIUM: 2,
            SPEED_LOW: 1,
            SPEED_OFF: 0
        }
        await self._fan.set_current_speed(speed_map[speed])

    @property
    def name(self):
        """Return the name of the fan."""
        return self._fan.name
