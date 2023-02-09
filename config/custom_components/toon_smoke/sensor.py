"""
Support for reading Smoke detector data through Eneco's Toon thermostats.
Only works for rooted Toon.

configuration.yaml

sensor:
  - platform: toon_smoke
    host: IP_ADDRESS
    port: 10080
    scan_interval: 10
    resources:
      - smoke01connected
      - smoke01alarmstatus
      - smoke01temperature
      - smoke01battery
      - smoke01tampering
      - smoke02connected
      - smoke02alarmstatus
      - smoke02temperature
      - smoke02battery
      - smoke02tampering
"""
import logging
from datetime import timedelta
import requests
import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
from homeassistant.const import (
    CONF_HOST, CONF_PORT, CONF_SCAN_INTERVAL, CONF_RESOURCES)
from homeassistant.util import Throttle
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

BASE_URL = 'http://{0}:{1}{2}'
MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=10)

SENSOR_PREFIX = 'Toon '

SENSOR_TYPES = {
    'smoke01connected': ['Smoke Sensor 1 Connected', '', 'mdi:broadcast'],
    'smoke01alarmstatus': ['Smoke Sensor 1 Alarm Status', '', 'mdi:smoke-detector'],
    'smoke01temperature': ['Smoke Sensor 1 Temperature', 'C', 'mdi:thermometer'],
    'smoke01battery': ['Smoke Sensor 1 Battery Level', '%', 'mdi:battery'],
    'smoke01tampering': ['Smoke Sensor 1 Tampering Detected', '', 'mdi:alert-octagram'],
    'smoke02connected': ['Smoke Sensor 2 Connected', '', 'mdi:broadcast'],
    'smoke02alarmstatus': ['Smoke Sensor 2 Alarm Status', '', 'mdi:smoke-detector'],
    'smoke02temperature': ['Smoke Sensor 2 Temperature', 'C', 'mdi:thermometer'],
    'smoke02battery': ['Smoke Sensor 2 Battery Level', '%', 'mdi:battery'],
    'smoke02tampering': ['Smoke Sensor 2 Tampering Detected', '', 'mdi:alert-octagram'],
}

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Optional(CONF_PORT, default=10800): cv.positive_int,
    vol.Required(CONF_RESOURCES, default=[]):
        vol.All(cv.ensure_list, [vol.In(SENSOR_TYPES)]),
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Setup the Toon smoke sensors."""
    scan_interval = config.get(CONF_SCAN_INTERVAL)
    host = config.get(CONF_HOST)
    port = config.get(CONF_PORT)

    try:
        data = ToonData(host, port)
    except requests.exceptions.HTTPError as error:
        _LOGGER.error(error)
        return False

    entities = []

    for resource in config[CONF_RESOURCES]:
        sensor_type = resource.lower()

        if sensor_type not in SENSOR_TYPES:
            SENSOR_TYPES[sensor_type] = [
                sensor_type.title(), '', 'mdi:flash']

        entities.append(ToonSmokeSensor(data, sensor_type))

    add_entities(entities)


# pylint: disable=abstract-method
class ToonData(object):
    """Representation of a Toon thermostat."""

    def __init__(self, host, port):
        """Initialize the thermostat."""
        self._host = host
        self._port = port
        self.data = None

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Update the data from the thermostat."""
        try:
            self.data = requests.get(BASE_URL.format(self._host, self._port, '/hdrv_zwave?action=getDevices.json'), timeout=5).json()
            _LOGGER.debug("Data = %s", self.data)
        except requests.exceptions.RequestException:
            _LOGGER.error("Error occurred while fetching data.")
            self.data = None
            return False


class ToonSmokeSensor(Entity):
    """Representation of a SmartMeter connected to Toon."""

    def __init__(self, data, sensor_type):
        """Initialize the sensor."""
        self.data = data
        self.type = sensor_type
        self._name = SENSOR_PREFIX + SENSOR_TYPES[self.type][0]
        self._unit = SENSOR_TYPES[self.type][1]
        self._icon = SENSOR_TYPES[self.type][2]
        self._state = None

        self._discovery = True
        self._dev_id = {}

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return self._icon

    @property
    def state(self):
        """Return the state of the sensor. """
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return self._unit

    def update(self):
        """Get the latest data and use it to update our sensor state."""
        self.data.update()
        energy = self.data.data

        """Go to http://toon.ip:port/hdrv_zwave?action=getDevices.json and search for dev_"""

        if self.type == 'smoke01connected':
            if 'dev_3' in energy:
                self._state = energy["dev_3"]["IsConnected"]

        elif self.type == 'smoke01alarmstatus':
            if 'dev_3' in energy:
                self._state = energy["dev_3"]["AlarmStatus"]

        elif self.type == 'smoke01temperature':
            if 'dev_3' in energy:
                self._state = energy["dev_3"]["CurrentTemperature"]

        elif self.type == 'smoke01battery':
            if 'dev_3' in energy:
                self._state = energy["dev_3"]["CurrentBatteryLevel"]

        elif self.type == 'smoke01tampering':
            if 'dev_3' in energy:
                self._state = energy["dev_3"]["TamperingDetected"]

        elif self.type == 'smoke02connected':
            if 'dev_6' in energy:
                self._state = energy["dev_6"]["IsConnected"]

        elif self.type == 'smoke02alarmstatus':
            if 'dev_6' in energy:
                self._state = energy["dev_6"]["AlarmStatus"]

        elif self.type == 'smoke02temperature':
            if 'dev_6' in energy:
                self._state = energy["dev_6"]["CurrentTemperature"]

        elif self.type == 'smoke02battery':
            if 'dev_6' in energy:
                self._state = energy["dev_6"]["CurrentBatteryLevel"]

        elif self.type == 'smoke02tampering':
            if 'dev_6' in energy:
                self._state = energy["dev_6"]["TamperingDetected"]