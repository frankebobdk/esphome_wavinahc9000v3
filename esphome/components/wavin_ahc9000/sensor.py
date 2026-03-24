import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor
from esphome.const import (
    CONF_DEVICE_CLASS,
    CONF_UNIT_OF_MEASUREMENT,
    CONF_ICON,
    CONF_ACCURACY_DECIMALS,
    UNIT_PERCENT,
    UNIT_DECIBEL_MILLIWATT,
    DEVICE_CLASS_BATTERY,
    DEVICE_CLASS_SIGNAL_STRENGTH,
    ICON_BATTERY,
    DEVICE_CLASS_TEMPERATURE,
    UNIT_CELSIUS,
)

from . import WavinAHC9000

CONF_PARENT_ID = "wavin_ahc9000_id"
CONF_CHANNEL = "channel"


CONF_TYPE = "type"

SENSOR_TYPES = [
    "battery", "temperature", "comfort_setpoint",
    "floor_temperature", "floor_min_temperature", "floor_max_temperature",
    "rssi", "alarm_low_temperature", "alarm_high_temperature",
]

CONFIG_SCHEMA = sensor.sensor_schema().extend(
    {
        cv.GenerateID(CONF_PARENT_ID): cv.use_id(WavinAHC9000),
        cv.Required(CONF_CHANNEL): cv.int_range(min=1, max=16),
        cv.Required(CONF_TYPE): cv.one_of(*SENSOR_TYPES, lower=True),
    }
)


async def to_code(config):
    hub = await cg.get_variable(config[CONF_PARENT_ID])

    # Inject defaults before new_sensor() reads them from config
    if config[CONF_TYPE] == "battery":
        config.setdefault(CONF_DEVICE_CLASS, DEVICE_CLASS_BATTERY)
        config.setdefault(CONF_UNIT_OF_MEASUREMENT, UNIT_PERCENT)
        config.setdefault(CONF_ICON, ICON_BATTERY)
        config.setdefault(CONF_ACCURACY_DECIMALS, 0)
    elif config[CONF_TYPE] == "rssi":
        config.setdefault(CONF_DEVICE_CLASS, DEVICE_CLASS_SIGNAL_STRENGTH)
        config.setdefault(CONF_UNIT_OF_MEASUREMENT, UNIT_DECIBEL_MILLIWATT)
        config.setdefault(CONF_ACCURACY_DECIMALS, 1)
    else:
        config.setdefault(CONF_DEVICE_CLASS, DEVICE_CLASS_TEMPERATURE)
        config.setdefault(CONF_UNIT_OF_MEASUREMENT, UNIT_CELSIUS)
        config.setdefault(CONF_ACCURACY_DECIMALS, 1)

    sens = await sensor.new_sensor(config)

    # Register with hub
    if config[CONF_TYPE] == "battery":
        cg.add(hub.add_channel_battery_sensor(config[CONF_CHANNEL], sens))
    elif config[CONF_TYPE] == "comfort_setpoint":
        cg.add(hub.add_channel_comfort_setpoint_sensor(config[CONF_CHANNEL], sens))
    elif config[CONF_TYPE] == "floor_temperature":
        cg.add(hub.add_channel_floor_temperature_sensor(config[CONF_CHANNEL], sens))
    elif config[CONF_TYPE] == "floor_min_temperature":
        cg.add(hub.add_channel_floor_min_temperature_sensor(config[CONF_CHANNEL], sens))
    elif config[CONF_TYPE] == "floor_max_temperature":
        cg.add(hub.add_channel_floor_max_temperature_sensor(config[CONF_CHANNEL], sens))
    elif config[CONF_TYPE] == "rssi":
        cg.add(hub.add_channel_rssi_sensor(config[CONF_CHANNEL], sens))
    elif config[CONF_TYPE] == "alarm_low_temperature":
        cg.add(hub.add_channel_alarm_low_sensor(config[CONF_CHANNEL], sens))
    elif config[CONF_TYPE] == "alarm_high_temperature":
        cg.add(hub.add_channel_alarm_high_sensor(config[CONF_CHANNEL], sens))
    else:
        cg.add(hub.add_channel_temperature_sensor(config[CONF_CHANNEL], sens))

    cg.add(hub.add_active_channel(config[CONF_CHANNEL]))
