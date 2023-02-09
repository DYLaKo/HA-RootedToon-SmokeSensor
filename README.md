# Home Assistant Custom Component for Rooted Toon Smoke Sensors

This is a Custom Component for Home-Assistant (https://home-assistant.io) reads and displays sensor values from the smoke sensors connected to a rooted Eneco Toon thermostat.

The Custom Component is a modified version of the smart meter sensor component created by cyberjunky (https://github.com/cyberjunky/home-assistant-toon_smartmeter)

NOTE: This component only works with rooted Eneco Toon devices.



# configuration.yaml 

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
