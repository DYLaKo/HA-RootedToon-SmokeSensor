# Home Assistant Custom Component for Rooted Toon Smoke Sensors

This is a Custom Component for Home-Assistant (https://home-assistant.io) reads and displays sensor values from the smoke sensors connected to a rooted Eneco Toon thermostat.

The Custom Component is a modified version of the smart meter sensor component created by cyberjunky (https://github.com/cyberjunky/home-assistant-toon_smartmeter). This version should work for 2 smoke sensors. 

NOTE: This component only works with rooted Eneco Toon devices.

## Installation

## Custom Component
- Copy directory `config/custom_components/toon_smoke` to your `<config dir>/custom_components` directory.
- Configure with config below.
- Restart Home-Assistant.


## Configuration
To use this component in your installation, add the following to your `configuration.yaml` file:

```yaml
# Example configuration.yaml entry
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
```

Configuration variables:

- **host** (*Required*): The IP address on which the Toon can be reached.
- **port** (*Optional*): Port used by your Toon. (default = 80 or 10080)
- **scan_interval** (*Optional*): Number of seconds between polls. (default = 10)
- **resources** (*Required*): This section tells the component which values to display.
