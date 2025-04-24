# pizero-ha-mqtt-sensor
Raspberry pi based mqtt sensor for Home Asistant

Tested on:
    
    Raspberry Pi Zero
    Raspbian GNU/Linux 12 (bookworm)
    Debian: 12.8
    Kernel: Linux 6.6.51+rpt-rpi-v6
    24.04.2025

## Prepare hardware

1. Connect BME280 sensor to i2c pins
2. Connect MH-Z19 sensor to GPIO17

 TODO: image pinout + table

## Install software

1. Git clone this repo
2. Run `./install.sh` script (sudo required)
3. Configure Home Asistant

## (Optional) Uninstall

1. Run `./uninstall-service.sh` script (sudo required)
2. Remove entire folder

## Configuring Home Asistant

Add MQTT Mosquitto broker to Home Asistant and setup/test it.

Add to configuration.yaml:
```yaml
mqtt:
  sensor:
    - name: "BME280 Temperature"
      state_topic: "home/sensors/bme280"
      unit_of_measurement: "°C"
      value_template: "{{ value_json.temperature }}"

    - name: "BME280 Humidity"
      state_topic: "home/sensors/bme280"
      unit_of_measurement: "%"
      value_template: "{{ value_json.humidity }}"

    - name: "BME280 Pressure"
      state_topic: "home/sensors/bme280"
      unit_of_measurement: "hPa"
      value_template: "{{ value_json.pressure }}"
      
    - name: "Sensor CO2"
      state_topic: "home/sensors/bme280"
      unit_of_measurement: "ppm"
      value_template: "{{ value_json.co2 }}"
      

recorder:
  purge_keep_days: 7000

history:

logbook:
```

`recorder`, `history` and `logbook` are optional and required to keep sensors values history.
